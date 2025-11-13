from datetime import datetime
from typing import Dict
import pandas as pd
from argentina_prod.pipeline.global_pipeline import GlobalPipeline


def filter_by_date_range(pipeline, start_date: datetime, end_date: datetime) -> GlobalPipeline:
    for attr_name in dir(pipeline):
        if attr_name.startswith('_') and not attr_name.startswith('__'):
            attr_value = getattr(pipeline, attr_name)

            if isinstance(attr_value, pd.DataFrame) and attr_value is not None:
                try:
                    filtered_df = attr_value[
                        (attr_value.index >= start_date) &
                        (attr_value.index <= end_date)
                        ]
                    setattr(pipeline, attr_name, filtered_df)
                except Exception as e:
                    raise ValueError(f"Error filtering {attr_name}: {e}")

    pipeline.start_date = start_date
    pipeline.end_date = end_date

    return pipeline


def run_chain_model(pipeline, model_sequence_config=None):
    """
    Lazily imports and runs the EndToEndModelRunner
    Only imports the module when the function is called
    """
    from argentina_prod.end_to_end_model_run import EndToEndModelRunner

    runner = EndToEndModelRunner(
        pipeline=pipeline,
        model_sequence_config_override=model_sequence_config
    )
    runner.run_all_models()

    return pipeline