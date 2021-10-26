from flask import Flask
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client.core import GaugeMetricFamily
import pandas as pd
import numpy as np
import sys
import os


class BackBlazeExporter(object):
    """ Convertor data from baidu excel to metrics which prometheus supports """

    def __init__(self, data_path):
        # DataFrame
        print(f" * {self.__class__} - reading data from {data_path}, it may take quite a while")
        self.data = self.load_data(data_path)
        # List
        self.columns = self.data.columns
        self.feature_offset = 5
        self.current_row = 0
        self.name_current = 'collectd_smart_smart_attribute_current'
        self.name_pretty = 'collectd_smart_smart_attribute_pretty'
        self.desc_current = "Collectd_exporter: 'smart'  Type: 'smart_attribute' Dstype: 'api.Gauge' Dsname: 'current'"
        self.desc_pretty = "Collectd_exporter: 'smart'  Type: 'smart_attribute' Dstype: 'api.Gauge' Dsname: 'pretty'"
        self.labels = ['instance', 'smart', 'type']
        self.instance = 'localhost'
        self.device = 'sda'
    
    def load_data(self, data_path):
        temp = pd.read_csv(data_path)
        temp = temp.fillna(temp.mean())
        temp = temp.fillna(0)
        return temp

    def collect(self):
        # app.logger.error(id(self.data))
        app.logger.error(f'the current row is {self.current_row}')
        row = self.data.iloc[self.current_row]

        metric_current = GaugeMetricFamily(name=self.name_current, documentation=self.desc_current, labels=self.labels)
        metric_pretty = GaugeMetricFamily(name=self.name_pretty, documentation=self.desc_pretty, labels=self.labels)

        
        for i, v in row.items():
            attr_name = i
            if self.columns.get_loc(attr_name) < self.feature_offset:
                continue
            labels = [self.instance, self.device, attr_name]
            value = 0 if np.isnan(v) else v # required to remove
            if attr_name.endswith('raw'):
                metric_pretty.add_metric(labels, value)
            else:
                 metric_current.add_metric(labels, value)
        yield metric_current
        yield metric_pretty
        self.current_row += 1


app = Flask(__name__)
exporter = PrometheusMetrics(app)


@app.route('/favicon.ico')
@exporter.do_not_track()
def favicon():
    return 'ok'


@app.route('/')
@exporter.do_not_track()
def main():
    """ context root """
    return """
        <html>
            <head><title>BackBlaze Exporter</title></head>
            <body>
                <h1>BackBlaze Exporter</h1>
                <p><a href='/metrics'>Metrics</a></p>
            </body>
        </html>
    """


if __name__ == '__main__':
    file_path = os.environ.get('path')
    if file_path is None:
        print('[ERROR] path is not defined')
        sys.exit(1)
    exporter.registry.register(BackBlazeExporter(file_path))
    app.run(host='0.0.0.0', port='8002')
