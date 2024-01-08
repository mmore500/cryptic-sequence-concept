#pragma once
#ifndef CSEQ_CONFIG_TRY_READ_CONFIG_FILE_HPP_INCLUDE
#define CSEQ_CONFIG_TRY_READ_CONFIG_FILE_HPP_INCLUDE

#include <cstdlib>
#include <filesystem>
#include <iostream>

#include "Config.hpp"

namespace cseq {

void try_read_config_file(cseq::Config & config, emp::ArgManager & am) {
  if(std::filesystem::exists("cseq.cfg")) {
    std::cout << "Configuration read from cseq.cfg" << '\n';
    config.Read("cseq.cfg");
  }
  am.UseCallbacks();
  if (am.HasUnused())
    std::exit(EXIT_FAILURE);
}

} // namespace cseq

#endif // #ifndef CSEQ_CONFIG_TRY_READ_CONFIG_FILE_HPP_INCLUDE
