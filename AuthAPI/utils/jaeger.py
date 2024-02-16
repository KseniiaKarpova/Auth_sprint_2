from core import config
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (BatchSpanProcessor,
                                            ConsoleSpanExporter)

settings = config.APPSettings()


class our_tracer():
    def __enter__(self):
        return True

    def __exit__(self, exc_type, exc_value, traceback):
        return True

    def start_as_current_span(self, text: str):
        return our_tracer()


if settings.jaeger.enable:
    tracer = trace.get_tracer(__name__)
else:
    tracer = our_tracer()


def configure_tracer(host, port, service_name) -> None:
    resource = Resource(attributes={
        "service.name": service_name
    })

    trace.set_tracer_provider(TracerProvider(resource=resource))
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(
            JaegerExporter(
                agent_host_name=host,
                agent_port=port,
            )
        )
    )
    # Чтобы видеть трейсы в консоли
    trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
