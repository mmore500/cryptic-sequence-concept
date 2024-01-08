#include <iostream>

#include "Empirical/include/emp/base/vector.hpp"

#include "cseq/config/Config.hpp"
#include "cseq/config/setup_config_native.hpp"
#include "cseq/example.hpp"

// This is the main function for the NATIVE version of Cryptic Sequence Complexity Concept.

cseq::Config cfg;

int main(int argc, char* argv[]) {
  // Set up a configuration panel for native application
  setup_config_native(cfg, argc, argv);
  cfg.Write(std::cout);

  std::cout << "Hello, world!" << "\n";

  return cseq::example();
}
