#pragma once
#ifndef CSEQ_CONFIG_SETUP_CONFIG_NATIVE_HPP_INCLUDE
#define CSEQ_CONFIG_SETUP_CONFIG_NATIVE_HPP_INCLUDE

#include "Empirical/include/emp/config/ArgManager.hpp"

#include "try_read_config_file.hpp"

namespace cseq {

void setup_config_native(cseq::Config & config, int argc, char* argv[]) {
  auto specs = emp::ArgManager::make_builtin_specs(&config);
  emp::ArgManager am(argc, argv, specs);
  cseq::try_read_config_file(config, am);
}

} // namespace cseq

#endif // #ifndef CSEQ_CONFIG_SETUP_CONFIG_NATIVE_HPP_INCLUDE
