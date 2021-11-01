from flask import Flask
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client.core import GaugeMetricFamily
import pandas as pd
import numpy as np
import sys
import os


WIKI_NAMES = {
    'Raw Read Error Rate': 'read-error-rate-normal',
    'SpinUpTime': 'spin-up-time-normal',
    'Reallocated Sector Count': 'reallocated-sectors-count-normal',
    'Seek Error Rate': 'seek-error-rate-normal',
    'Power on Hours': 'power-on-hours-normal',
    'Reported Uncorrectable Error': 'reported-uncorrectable-errors-normal',
    'High Fly Writes': 'high-fly-writes-normal',
    'Temperature Celsius': 'temperature-normal',
    'Hardware ECC Recovered': 'hardware-ecc-recovered-normal',
    'Current Pending Sector': 'current-pending-sector-count-normal',
    'Reallocated Sectors Count': 'reallocated-sectors-count-raw',
    'Current Pending Sectors counts': 'current-pending-sector-count-raw'}


class BaiduExporter(object):
    """ Convertor data from baidu excel to metrics which prometheus supports """

    def __init__(self, data_path):
        # DataFrame
        print(f" * {self.__class__} - reading data from {data_path}, it may take quite a while")
        self.data = pd.read_csv(data_path)
        self.data = self.data[self.data['Drive Status'] == -1]
        print(self.data['Drive Status'])
        # List
        self.columns = self.data.columns
        self.feature_offset = 2
        self.current_row = 0
        self.name_current = 'collectd_smart_smart_attribute_current'
        self.name_pretty = 'collectd_smart_smart_attribute_pretty'
        self.desc_current = "Collectd_exporter: 'smart'  Type: 'smart_attribute' Dstype: 'api.Gauge' Dsname: 'current'"
        self.desc_pretty = "Collectd_exporter: 'smart'  Type: 'smart_attribute' Dstype: 'api.Gauge' Dsname: 'pretty'"
        self.labels = ['instance', 'smart', 'type']
        self.instance = 'localhost'
        self.device = 'sda'

    def collect(self):
        # app.logger.error(id(self.data))
        app.logger.error(f'the current row is {self.current_row}')
        row = self.data.iloc[self.current_row]

        metric_current = GaugeMetricFamily(name=self.name_current, documentation=self.desc_current, labels=self.labels)
        metric_pretty = GaugeMetricFamily(name=self.name_pretty, documentation=self.desc_pretty, labels=self.labels)

        for i, v in row.items():
            attr_name = WIKI_NAMES.get(i)
            if attr_name is None:
                continue
            labels = [self.instance, self.device, attr_name]
            value = 0 if np.isnan(v) else v
            value = 0 if value == -1 else ((value + 1) * 253 / 2)
            # TODO 12 processing
            if i in self.columns[self.feature_offset:12]:
                metric_current.add_metric(labels, value)
            else:
                metric_pretty.add_metric(labels, value)
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
            <head><title>Baidu Exporter</title></head>
            <body>
                <h1>Baidu Exporter</h1>
                <p><a href='/metrics'>Metrics</a></p>
            </body>
        </html>
    """


if __name__ == '__main__':
    file_path = os.environ.get('path')
    if file_path is None:
        print('[ERROR] path is not defined')
        sys.exit(1)
    exporter.registry.register(BaiduExporter(file_path))
    app.run(host='0.0.0.0', port='8000')
