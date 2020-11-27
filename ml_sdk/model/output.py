from dataclasses import dataclass


@dataclass
class Output:
    data: dict


@dataclass
class InferenceOutput(Output):
    pass


@dataclass
class ReportOutput(Output):
    pass