#pragma once
#ifndef CSEQ_CONFIG_SETUP_CONFIG_WEB_HPP_INCLUDE
#define CSEQ_CONFIG_SETUP_CONFIG_WEB_HPP_INCLUDE

#include "Empirical/include/emp/config/ArgManager.hpp"
#include "Empirical/include/emp/web/UrlParams.hpp"
#include "Empirical/include/emp/web/web.hpp"

#include "Config.hpp"
#include "try_read_config_file.hpp"

namespace cseq {

void setup_config_web(cseq::Config & config)  {
  auto specs = emp::ArgManager::make_builtin_specs(&config);
  emp::ArgManager am(emp::web::GetUrlParams(), specs);
  cseq::try_read_config_file(config, am);
}

} // namespace cseq

#endif // #ifndef CSEQ_CONFIG_SETUP_CONFIG_WEB_HPP_INCLUDE
