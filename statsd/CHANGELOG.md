# CHANGELOG - statsd

<!-- towncrier release notes start -->

## 1.12.0 / 2024-01-05

***Added***:

* Bump the Python version from py3.9 to py3.11 ([#15997](https://github.com/DataDog/integrations-core/pull/15997))

## 1.11.1 / 2023-08-18 / Agent 7.48.0

***Fixed***:

* Update datadog-checks-base dependency version to 32.6.0 ([#15604](https://github.com/DataDog/integrations-core/pull/15604))

## 1.11.0 / 2023-08-10

***Added***:

* Update generated config models ([#15212](https://github.com/DataDog/integrations-core/pull/15212))

***Fixed***:

* Fix types for generated config models ([#15334](https://github.com/DataDog/integrations-core/pull/15334))

## 1.10.1 / 2023-07-10 / Agent 7.47.0

***Fixed***:

* Bump Python version from py3.8 to py3.9 ([#14701](https://github.com/DataDog/integrations-core/pull/14701))

## 1.10.0 / 2022-04-05 / Agent 7.36.0

***Added***:

* Add metric_patterns options to filter all metric submission by a list of regexes ([#11695](https://github.com/DataDog/integrations-core/pull/11695))

## 1.9.0 / 2022-02-19 / Agent 7.35.0

***Added***:

* Add `pyproject.toml` file ([#11440](https://github.com/DataDog/integrations-core/pull/11440))

***Fixed***:

* Fix namespace packaging on Python 2 ([#11532](https://github.com/DataDog/integrations-core/pull/11532))

## 1.8.1 / 2022-01-08 / Agent 7.34.0

***Fixed***:

* Add comment to autogenerated model files ([#10945](https://github.com/DataDog/integrations-core/pull/10945))

## 1.8.0 / 2021-10-04 / Agent 7.32.0

***Added***:

* Disable generic tags ([#10027](https://github.com/DataDog/integrations-core/pull/10027))

## 1.7.1 / 2021-07-15 / Agent 7.30.0

***Fixed***:

* Allow float value for timeout ([#9711](https://github.com/DataDog/integrations-core/pull/9711))

## 1.7.0 / 2021-07-12

***Added***:

* Add runtime configuration validation ([#8990](https://github.com/DataDog/integrations-core/pull/8990))

## 1.6.1 / 2021-03-07 / Agent 7.27.0

***Fixed***:

* Bump minimum base package version ([#8443](https://github.com/DataDog/integrations-core/pull/8443))

## 1.6.0 / 2020-10-31 / Agent 7.24.0

***Added***:

* Add statsd logs ([#7773](https://github.com/DataDog/integrations-core/pull/7773))

## 1.5.0 / 2020-09-21 / Agent 7.23.0

***Added***:

* Add config specs ([#7481](https://github.com/DataDog/integrations-core/pull/7481))

## 1.4.0 / 2020-05-17 / Agent 7.20.0

***Added***:

* Allow optional dependency installation for all checks ([#6589](https://github.com/DataDog/integrations-core/pull/6589))

## 1.3.1 / 2020-04-04 / Agent 7.19.0

***Fixed***:

* Update deprecated imports ([#6088](https://github.com/DataDog/integrations-core/pull/6088))

## 1.3.0 / 2019-05-14 / Agent 6.12.0

***Added***:

* Adhere to code style ([#3570](https://github.com/DataDog/integrations-core/pull/3570))

## 1.2.0 / 2019-01-04 / Agent 6.9.0

***Added***:

* Support Python 3 ([#2831][1])

## 1.1.1 / 2018-09-04 / Agent 6.5.0

***Fixed***:

* Add data files to the wheel package ([#1727][2])

## 1.1.0 / 2018-05-11

***Added***:

* Add timeout configuration.

## 1.0.0 / 2017-03-22

***Added***:

* adds statsd integration.

[1]: https://github.com/DataDog/integrations-core/pull/2831
[2]: https://github.com/DataDog/integrations-core/pull/1727
