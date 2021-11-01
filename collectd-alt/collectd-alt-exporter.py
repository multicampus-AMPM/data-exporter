from flask import Flask
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client.core import GaugeMetricFamily
import pandas as pd
import os


DATA = {
    'current': {
        "wear-range-delta": 98.0,
        "used-reserved-block-count-total": 100.0,
        "program-fail-count-total": 100.0,
        "erase-fail-count": 100.0,
        "sata-downshift-error-count": 100.0,
        "reported-uncorrectable-errors": 100.0,
        "temperature-difference": 71.0,
        "hardware-ecc-recovered": 200.0,
        "ultradma-crc-error-count": 100.0,
        "good-block-count-and-system(free)-block-count": 99.0,
        "total-lbas-written": 99.0,
        "total-lbas-read": 99.0,
        "reallocated-sectors-count": 100.0,
        "power-on-hours": 99.0,
        "power-cycle-count": 98.0
    },
    'pretty': {
        "wear-range-delta": 98.0,
        "used-reserved-block-count-total": 100.0,
        "program-fail-count-total": 0.0,
        "erase-fail-count": 0.0,
        "sata-downshift-error-count": 0.0,
        "reported-uncorrectable-errors": 0.0,
        "temperature-difference": 302150.0,
        "hardware-ecc-recovered": 0.0,
        "ultradma-crc-error-count": 0.0,
        "good-block-count-and-system(free)-block-count": 0.0,
        "total-lbas-written": 267495162970,
        "total-lbas-read": 266426040987,
        "poweron": 7639200,
        "powercycles": 1066.0,
        "badsectors": 0.0,
        "temperature": 29.0,
        "reallocated-sectors-count": 0.0,
        "power-on-hours": 7639200000,
        "power-cycle-count": 1066.0
    }
}


class CollectdAltExporter(object):

    def __init__(self):
        self.name_current = 'collectd_smart_smart_attribute_current'
        self.name_pretty = 'collectd_smart_smart_attribute_pretty'
        self.desc_current = "Collectd_exporter: 'smart'  Type: 'smart_attribute' Dstype: 'api.Gauge' Dsname: 'current'"
        self.desc_pretty = "Collectd_exporter: 'smart'  Type: 'smart_attribute' Dstype: 'api.Gauge' Dsname: 'pretty'"
        self.labels = ['instance', 'smart', 'type']
        self.instance = 'localhost'
        self.drive = 'sda'
    
    def collect(self):
        metric_current = GaugeMetricFamily(name=self.name_current, documentation=self.desc_current, labels=self.labels)
        current = DATA['current']
        for key, value in current.items():
            labels = [self.instance, self.drive, key]
            metric_current.add_metric(labels, value)
        yield metric_current

        metric_pretty = GaugeMetricFamily(name=self.name_pretty, documentation=self.desc_pretty, labels=self.labels)
        pretty = DATA['pretty']
        for key, value in pretty.items():
            labels = [self.instance, self.drive, key]
            metric_pretty.add_metric(labels, value)
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
            <head><title>Collectd Exporter</title></head>
            <body>
                <h1>Collectd Exporter</h1>
                <p><a href='/metrics'>Metrics</a></p>
            </body>
        </html>
    """


if __name__ == '__main__':
    # app에 debug=True 파라미터 그냥 전달하면 /metrics 맵핑 안됨
    # DEBUG_METRICS 환경변수 추가 필요
    # https://github.com/rycus86/prometheus_flask_exporter/issues/40
    os.environ['DEBUG_METRICS'] = 'true'
    exporter.registry.register(CollectdAltExporter())
    app.run(host='0.0.0.0', port='9103', debug=True)