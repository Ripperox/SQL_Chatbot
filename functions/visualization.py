from lida import llm, Manager, TextGenerationConfig
from logger import logger

lida = Manager(text_gen=llm("openai"))
textgen_config = TextGenerationConfig(n=1, temperature=0.2, use_cache=True)
library ="seaborn"
def visualizer(dataframe, query):
    summary = lida.summarize(dataframe, summary_method="llm", textgen_config=textgen_config, n_samples=3)
    try:
        charts = lida.visualize(summary=summary, goal=query, textgen_config=textgen_config, library=library)
        if charts and hasattr(charts[0], 'raster'):
            return charts[0], summary
        else:
            raise AttributeError("No raster attribute found in charts")
    except Exception as e:
        repaired_charts, repaired_summary = repair(charts, query, summary, error=str(e))
        if repaired_charts and hasattr(repaired_charts[0], 'raster'):
            return repaired_charts[0], repaired_summary
        else:
            return "Error in visualizing data: " + str(repaired_charts), repaired_summary

def repair(charts, query, summary, error):
    try:
        feedback = f"""
        You are a helpful assistant highly skilled in revising visualization code to improve the quality of the code and visualization based on feedback. Assume that data in plot(data) contains a valid dataframe.
        You MUST return a full program. DO NOT include any preamble text. Do not include explanations or prose. The error given was {error}.
        """
        repaired_code = lida.repair(
            code=charts,
            feedback=feedback,
            goal=query,
            summary=summary,
            textgen_config=textgen_config,
            library=library,
            return_error=True
        )
        if repaired_code and 'error' not in repaired_code:
            return repaired_code, summary  # Return repaired code if successful and no errors
        else:
            error_msg = "Failed to repair code: " + str(repaired_code)
            logger.error(error_msg)
            return "Error in visualizing data: " + error_msg, summary
    except Exception as e:
        error_msg = "Error in repairing visualization code: " + str(e)
        logger.error(error_msg)
        return error_msg, summary

def edit(charts, specifications, summary):
    textgen_config = TextGenerationConfig(n=1, temperature=0, use_cache=True)
    try:
        edited_charts = lida.edit(
            code=charts,
            summary=summary,
            instructions=specifications,
            textgen_config=textgen_config,
            library=library
        )
        if edited_charts and hasattr(edited_charts[0], 'raster'):
            return edited_charts[0], summary
        else:
            raise AttributeError("No raster attribute found in edited charts")
    except Exception as e:
        return repair(charts, specifications, summary, error=str(e))

