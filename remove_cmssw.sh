#! /bin/bash

# load installation environment from a bootstrapped area
function load_bootstrap_environment() {
  test -n "$1" || return 1

  # set the environment
  export http_proxy="http://cmsproxy.cms:3128/"
  export https_proxy="https://cmsproxy.cms:3128/"
  export NO_PROXY=".cms"
  export VO_CMS_SW_DIR="$(readlink -f $1)"
  export LANG="C"
  test -n "$SCRAM_ARCH" || SCRAM_ARCH=slc6_amd64_gcc481
  export SCRAM_ARCH

  # check that the area has been bootstrapped
  if ! [ -f "$VO_CMS_SW_DIR"/"$SCRAM_ARCH"/external/apt/*/etc/profile.d/init.sh ]; then
    echo "Can only load the environment from an already bootstrapped area"
    return 1
  fi

  source "$VO_CMS_SW_DIR"/"$SCRAM_ARCH"/external/apt/*/etc/profile.d/init.sh
  apt-get update
}

# some git stuff
# boostrap a new CMSSW area
function bootstrap_cmssw() {
  test -n "$1" || return 1

  # set the environment
  export http_proxy="http://cmsproxy.cms:3128/"
  export https_proxy="https://cmsproxy.cms:3128/"
  export NO_PROXY=".cms"
  export VO_CMS_SW_DIR="$(readlink -f $1)"
  export LANG="C"
  test -n "$SCRAM_ARCH" || SCRAM_ARCH=slc6_amd64_gcc481
  export SCRAM_ARCH

  # if necessary, bootstrap the area
  if ! [ -f "$VO_CMS_SW_DIR"/"$SCRAM_ARCH"/external/apt/*/etc/profile.d/init.sh ]; then
    mkdir -p "$VO_CMS_SW_DIR"
    echo "Downloading bootstrap script"
    wget -q -O "$VO_CMS_SW_DIR"/bootstrap.sh http://cmsrep.cern.ch/cmssw/cms/bootstrap.sh
    chmod +x "$VO_CMS_SW_DIR"/bootstrap.sh

    echo "Bootstrapping software area at $VO_CMS_SW_DIR"
    "$VO_CMS_SW_DIR"/bootstrap.sh setup -path "$VO_CMS_SW_DIR" -arch "$SCRAM_ARCH" 2>&1 | tee "$VO_CMS_SW_DIR"/bootstrap_"$SCRAM_ARCH".log
    if (( $? )); then
      echo
      echo "Bootstrap failed"
      return 1
    fi
    echo "Acquire::Retries 99;" >> "$VO_CMS_SW_DIR"/"$SCRAM_ARCH"/external/apt/*/etc/apt.conf

    # make the IBs available
    echo "rpm http://cmsrep.cern.ch cmssw/cms.week0/apt/$SCRAM_ARCH lcg cms external"       >> "$VO_CMS_SW_DIR"/"$SCRAM_ARCH"/external/apt/*/etc/sources.list
    echo "# rpm-src http://cmsrep.cern.ch cmssw/cms.week0/apt/$SCRAM_ARCH lcg cms external" >> "$VO_CMS_SW_DIR"/"$SCRAM_ARCH"/external/apt/*/etc/sources.list
    echo "rpm http://cmsrep.cern.ch cmssw/cms.week1/apt/$SCRAM_ARCH lcg cms external"       >> "$VO_CMS_SW_DIR"/"$SCRAM_ARCH"/external/apt/*/etc/sources.list
    echo "# rpm-src http://cmsrep.cern.ch cmssw/cms.week1/apt/$SCRAM_ARCH lcg cms external" >> "$VO_CMS_SW_DIR"/"$SCRAM_ARCH"/external/apt/*/etc/sources.list
  fi

  # optionally, install a CMSSW release
  test -n "$2" || return 0
  echo "Updataing package database"
  source "$VO_CMS_SW_DIR"/"$SCRAM_ARCH"/external/apt/*/etc/profile.d/init.sh
  apt-get update
  if echo $2 | grep -q patch; then
    echo "Installing patch release $2"
    apt-get -y -D remove cms+cmssw-patch+$2
    
    
  else
    echo "Installing release $2"
    apt-get -y -D remove cms+cmssw+$2
  fi
  apt-get clean
}

bootstrap_cmssw "$@"
