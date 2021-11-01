from flask import Flask
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client.core import GaugeMetricFamily
import pandas as pd
import os
import sys


class FailureExporter(object):

    def __init__(self, file_path, logger):
        self.data = self.get_data(file_path)
        self.logger = logger
        self.offset = 5
        self.current_row = -1
        self.length = self.data.shape[0] - 1
        self.columns = self.data.columns
        self.name_current = 'collectd_smart_smart_attribute_current'
        self.name_pretty = 'collectd_smart_smart_attribute_pretty'
        self.desc_current = "Collectd_exporter: 'smart'  Type: 'smart_attribute' Dstype: 'api.Gauge' Dsname: 'current'"
        self.desc_pretty = "Collectd_exporter: 'smart'  Type: 'smart_attribute' Dstype: 'api.Gauge' Dsname: 'pretty'"
        self.labels = ['instance', 'smart', 'type', 'index']
        self.instance = 'localhost'
        self.device = 'sda'

    def get_data(self, file_path):
        if file_path is None:
            raise FileNotFoundError(f"'{file_path} 'not found")
        data = pd.read_csv(file_path)
        # nan만 있는 컬럼 drop
        data.dropna(axis=1, how='all', inplace=True)
        # 결측치 0으로 치환
        data.fillna(0, inplace=True)
        return data
    
    def collect(self):
        metric_current = GaugeMetricFamily(name=self.name_current, documentation=self.desc_current, labels=self.labels)
        metric_pretty = GaugeMetricFamily(name=self.name_pretty, documentation=self.desc_pretty, labels=self.labels)
        if self.current_row > self.length:
            self.current_row = 0
        if self.current_row > -1:
            # 인스턴스 올라갈 때 값 들어가지 않도록 self.current_row 0부터 시작
            row = self.data.iloc[self.current_row]
            for index, value in row.items():
                if self.columns.get_loc(index) < self.offset:
                    continue
                attr_name = index.replace('-raw', '') if index.endswith('raw') else index.replace('-normal', '')
                labels = [self.instance, self.device, attr_name, str(self.current_row)]
                if index.endswith('raw'):
                    metric_pretty.add_metric(labels, value)
                else:
                    metric_current.add_metric(labels, value)
        self.current_row += 1
        yield metric_current
        yield metric_pretty


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
            <head><title>Failure Exporter</title></head>
            <body>
                <h1>Failure Exporter</h1>
                <p><a href='/metrics'>Metrics</a></p>
            </body>
        </html>
    """


if __name__ == '__main__':
    # app에 debug=True 파라미터 그냥 전달하면 /metrics 맵핑 안됨
    # DEBUG_METRICS 환경변수 추가 필요
    # https://github.com/rycus86/prometheus_flask_exporter/issues/40
    os.environ['DEBUG_METRICS'] = 'true'
    file_path = os.environ.get('path')
    exporter.registry.register(FailureExporter(file_path, app.logger))
    app.run(host='0.0.0.0', port='8002', debug=True)