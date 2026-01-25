from richard.core.Solver import Solver
from richard.entity.ProcessResult import ProcessResult
from richard.entity.SentenceRequest import SentenceRequest
from richard.interface.SomeComposer import SomeComposer
from richard.interface.SomeExecutor import SomeExecutor
from richard.interface.SomeGenerator import SomeGenerator
from richard.interface.SomeModel import SomeModel
from richard.interface.SomeParser import SomeParser
from richard.interface.SomeSystem import SomeSystem
from .Model import Model


class BasicSystem(SomeSystem):
    parser: SomeParser
    composer: SomeComposer
    executor: SomeExecutor
    output_generator: SomeGenerator
    model: SomeModel

    def __init__(self,
            model: SomeModel=None,
            parser: SomeParser=None,
            composer: SomeComposer=None,
            executor: SomeExecutor=None,
            output_generator: SomeGenerator=None):

        self.model = model if model else Model([])
        self.parser = parser
        self.composer = composer
        self.executor = executor
        self.output_generator = output_generator


    def enter(self, request: SentenceRequest):
        if not self.parser:
            return None

        parse_result = self.parser.process(request)
        if parse_result.error_type != "":
            return self.log_error(parse_result)

        if not self.composer:
            return parse_result

        for parse_product in parse_result.products:
            composer_result = self.composer.process(parse_product)
            if composer_result.error_type != "":
                return self.log_error(composer_result)

            if not self.executor:
                return composer_result

            for composer_product in composer_result.products:
                executor_result = self.executor.process(composer_product)
                if executor_result.error_type != "":
                    return self.log_error(executor_result)

                return executor_result.products[0].get_output()


    def log_error(self, result: ProcessResult):
        Solver(self.model).solve([('store', [
            ('output_type', result.error_type),
            ('output_' + result.error_type, *result.error_args)])])
        return result


    def read_output(self):
        return self.output_generator.generate_output()
