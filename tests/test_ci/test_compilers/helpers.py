# -*- coding: utf-8 -*-


from conan_sword_and_sorcery.parsers.profile import profile_for, parse_profile


class CompilerMixinTestCase:
    compiler_class = None

    def get_compiler_init_arguments(self):
        raise NotImplementedError

    def get_profile_file(self):
        raise NotImplementedError

    def test_id(self):
        kwargs = self.get_compiler_init_arguments()
        compiler = self.compiler_class(**kwargs)
        str_representation = str(compiler)
        for item in self.compiler_class._required_init_arguments:
            self.assertTrue(getattr(compiler, item) in str_representation, msg="Attribute '{}' not found in compiler repr '{}'".format(item, str_representation))

    def test_profile_file(self):
        kwargs = self.get_compiler_init_arguments()
        compiler = self.compiler_class(**kwargs)

        with profile_for(compiler) as ff:
            parser = parse_profile(ff)
            profile_true = self.get_profile_file()

            self.assertListEqual(parser.sections(), profile_true.sections())
            for section in parser.sections():
                self.assertDictEqual(dict(parser.items(section)), dict(profile_true.items(section)))
