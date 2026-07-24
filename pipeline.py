from logger import logger

class AnalysisPipeline:
    def __init__(self):
        self._stages: dict = {}
        logger.info("Initialized Analysis pipeline...")

    def add_stage(self, stage_name: str, stage: function):
        try:
            self._stages[stage_name] = stage
            logger.debug("Added stage {} with stage_name {}", stage, stage_name)
            return self
        except Exception:
            logger.exception("Exception in adding stage to pipeline stage={}", stage)
            raise

    def remove_stage(self, stage_name: str):
        try:
            self._stages.pop(stage_name)
            logger.debug("Removed stage {}", stage_name)
            return self
        except Exception:
            logger.exception("Exception in removing stage stage={}", stage_name)
            raise

def dummy(a,b):
    return a+b

def dummy_yummy():
    return "Hello"

pipeline = AnalysisPipeline()
pipeline.add_stage("preprocessing", dummy)