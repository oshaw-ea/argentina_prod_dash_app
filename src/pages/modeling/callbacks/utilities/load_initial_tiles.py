from argentina_prod.pipeline.global_pipeline import GlobalPipeline

from pages.modeling.callbacks.utilities.visual_builders.visuals_builders import VisualsBuilder
from pages.utilities import ChartTitles, pack_data


def load_initial_drilled_wells(pipeline: GlobalPipeline) -> tuple:
    drilled_wells_forecast = pipeline.drilled_wells_forecast
    drilled_wells_history = pipeline.drilled_wells_history
    drilled_wells_forecast = drilled_wells_forecast.loc[
        drilled_wells_forecast.index > max(drilled_wells_history.index)]

    drilled_wells_history, drilled_wells_forecast, drilled_wells_columns, drilled_wells_data, drilled_wells_fig = VisualsBuilder.process_and_visualise_data(
        history_df=drilled_wells_history,
        forecast_df=drilled_wells_forecast,
        title=ChartTitles.DRILLED_WELLS
    )
    packed_drilled_wells = pack_data(drilled_wells_history)

    return drilled_wells_history, drilled_wells_forecast, drilled_wells_columns, drilled_wells_data, packed_drilled_wells, drilled_wells_fig


def load_initial_completions(pipeline: GlobalPipeline) -> tuple:
    completions_history = pipeline.completions_history
    completions_forecast = pipeline.completions_forecast

    completions_history, completions_forecast, completions_columns, completions_data, completions_fig = VisualsBuilder.process_and_visualise_data(
        history_df=completions_history,
        forecast_df=completions_forecast,
        title=ChartTitles.COMPLETIONS
    )
    packed_completions_history = pack_data(completions_history)

    return completions_history, completions_forecast, completions_columns, completions_data, packed_completions_history, completions_fig


def load_data(pipeline):
    drilled_wells_history, drilled_wells_forecast, drilled_wells_columns, drilled_wells_data, drilled_wells_store, drilled_wells_fig = load_initial_drilled_wells(
        pipeline=pipeline,
    )

    completions_history, completions_forecast, completions_columns, completions_data, completions_store, completions_fig = load_initial_completions(
        pipeline=pipeline,
    )


    return (drilled_wells_history, drilled_wells_forecast, drilled_wells_columns, drilled_wells_data,
            drilled_wells_store, drilled_wells_fig,
            completions_history, completions_forecast, completions_columns, completions_data, completions_store,
            completions_fig)
