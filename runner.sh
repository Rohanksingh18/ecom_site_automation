
# This command enables the debug mode, which displays each command before it is executed. It is useful for debugging shell scripts as it provides visibility into the commands being executed.
set -x
#set -e

# This line assigns the value of the first command-line argument to the variable location.
location=$1
# This line assigns the value of the second command-line argument to the variable options.
options=$2

#to generate a timestamp
timestamp=`date "+%Y%m%d%H%M%S"`
output_dir=$(pwd)/output/${timestamp}
log_file=${output_dir}/pytest_log.log
html_report=${output_dir}/report.html
export RESULTS_DIR=${output_dir}
export DATA_DIRECTORY=$(pwd)/src/data

source variables_local.sh

python3 -m pytest \
${location} \
--log-file=${log_file} \
--log-file-level=info \
--log-level=info \
--log-cli-level=info \
--log-level=info \
--html=${html_report} \
--junitxml=$RESULTS_DIR/myjunit.xml \
${options}



echo  "Log File = ${log_file}"
echo  "HTML Report = ${html_report}"

