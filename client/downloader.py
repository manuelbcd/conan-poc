 # Sample downloaded from jfrog/conan hooks page 
 from conans import tools


 def pre_export(output, conanfile, conanfile_path, reference, **kwargs):
     test = "%s/%s" % (reference.name, reference.version)
     for field in ["url", "license", "description"]:
         field_value = getattr(conanfile, field, None)
         if not field_value:
             output.error("%s Conanfile doesn't have '%s'. It is recommended to add it as attribute: %s"
                         % (test, field, conanfile_path))

 def pre_source(output, conanfile, conanfile_path, **kwargs):
     conanfile_content = tools.load(conanfile_path)
     if "def source(self):" in conanfile_content:
         test = "[IMMUTABLE SOURCES]"
         valid_content = [".zip", ".tar", ".tgz", ".tbz2", ".txz"]
         invalid_content = ["git checkout master", "git checkout devel", "git checkout develop"]
         if "git clone" in conanfile_content and "git checkout" in conanfile_content:
             fixed_sources = True
             for invalid in invalid_content:
                 if invalid in conanfile_content:
                     fixed_sources = False
         else:
             fixed_sources = False
             for valid in valid_content:
                 if valid in conanfile_content:
                     fixed_sources = True

         if not fixed_sources:
             output.error("%s Source files does not come from and immutable place. Checkout to a "
                         "commit/tag or download a compressed source file for %s" % (test, str(reference)))
