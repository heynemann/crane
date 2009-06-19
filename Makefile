# Makefile for crane
SHELL := /bin/bash

# Internal variables.
file_version=0.1.0
root_dir=.
build_dir=${root_dir}/build
src_dir=${root_dir}/crane

tests_dir=${root_dir}/tests
unit_tests_dir=${tests_dir}/unit
functional_tests_dir=${tests_dir}/functional

compile_log_file=${build_dir}/compile.log
unit_log_file=${build_dir}/unit.log
functional_log_file=${build_dir}/functional.log

nocoverage=false

help:
	@echo
	@echo "    crane Makefile v${file_version}"
	@echo "    usage: make <target>"
	@echo
	@echo "    targets:"
	@echo "    help             displays this help text"
	@echo "    all              compiles the code and runs all tests"
	@echo "    clean            cleans the build directory"
	@echo "    compile          compiles the python code"
	@echo "    test             runs all tests (unit and functional)"
	@echo "    unit             runs all unit tests"
	@echo "    functional       runs all functional tests"
	@echo "    codeanalyis      generates code analysis info"
	@echo "    sdist            creates a source-based distribution"
	@echo "    deb              creates a debian-based distribution"
	@echo

# orchestrator targets

unit: prepare_build compile run_unit report_success
functional: prepare_build compile run_functional report_success

all: prepare_build compile test report_success

prepare_build: clean create_build_dir

test: run_unit run_functional

clean: remove_build_dir

# action targets

report_success:
	@echo "Build succeeded!"

remove_build_dir:
	@rm -fr ${build_dir}

create_build_dir:
	@mkdir -p ${build_dir}

compile:
	@echo "Compiling source code..."
	@rm -f ${compile_log_file} >> /dev/null
	@rm -f -r ${src_dir}/*.pyc >> /dev/null
	@python -m compileall ${src_dir}

run_unit: compile
	@echo "Running unit tests..."
	@rm -f ${unit_log_file} >> /dev/null
	@if [ "$(nocoverage)" = "true" ]; then nosetests --verbose ${unit_tests_dir}; else nosetests --verbose --with-coverage --cover-package=crane ${unit_tests_dir}; fi

run_functional: compile
	@echo "Running functional tests..."
	@rm -f ${functional_log_file} >> /dev/null
	@if [ "$(nocoverage)" = "true" ]; then nosetests --verbose ${functional_tests_dir}; else nosetests --verbose --with-coverage --cover-package=crane ${functional_tests_dir}; fi

codeanalysis:
	@echo "Generating code analysis..."
	@sloccount ${root_dir}

deb:
	@echo "=============================="
	@echo "Generating Debian Distribution"
	@echo "=============================="
	mv .git /tmp/crane_git
	debuild
	mkdir -p dist
	cp ../python-crane_* ./dist
	rm -f ../python-crane_*
	debuild clean
	mv /tmp/crane_git .git
