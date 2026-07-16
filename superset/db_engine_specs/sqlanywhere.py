# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
from __future__ import annotations

import logging

from superset.constants import TimeGrain
from superset.db_engine_specs.base import BaseEngineSpec, DatabaseCategory

logger = logging.getLogger(__name__)


class SqlAnywhereEngineSpec(BaseEngineSpec):
    """Engine spec for SAP SQL Anywhere"""

    engine = "sqlany"
    engine_name = "SAP SQL Anywhere"
    default_driver = "sqlanydb"

    metadata = {
        "description": (
            "SAP SQL Anywhere (formerly Sybase SQL Anywhere) "
            "is a relational database management system."
        ),
        "logo": "sybase.png",
        "homepage_url": "https://www.sap.com/products/technology-platform/sql-anywhere.html",
        "categories": [
            DatabaseCategory.TRADITIONAL_RDBMS,
            DatabaseCategory.PROPRIETARY,
        ],
        "pypi_packages": ["sqlalchemy-sqlany", "sqlanydb"],
        "connection_string": "sqlany+sqlanydb://{username}:{password}@{host}:{port}/{database}",
        "parameters": {
            "username": "Database username",
            "password": "Database password",
            "host": "Database host",
            "port": "Database port",
            "database": "Database name",
        },
        "notes": "Requires SQL Anywhere client libraries installed on the system.",
        "docs_url": "https://help.sap.com/docs/SAP_SQL_Anywhere",
    }

    _time_grain_expressions = {
        None: "{col}",
        TimeGrain.SECOND: "DATEADD(second, DATEDIFF(second, '2000-01-01', {col}), '2000-01-01')",  # noqa: E501
        TimeGrain.MINUTE: "DATEADD(minute, DATEDIFF(minute, '2000-01-01', {col}), '2000-01-01')",  # noqa: E501
        TimeGrain.FIVE_MINUTES: "DATEADD(minute, DATEDIFF(minute, '2000-01-01', {col}) / 5 * 5, '2000-01-01')",  # noqa: E501
        TimeGrain.TEN_MINUTES: "DATEADD(minute, DATEDIFF(minute, '2000-01-01', {col}) / 10 * 10, '2000-01-01')",  # noqa: E501
        TimeGrain.FIFTEEN_MINUTES: "DATEADD(minute, DATEDIFF(minute, '2000-01-01', {col}) / 15 * 15, '2000-01-01')",  # noqa: E501
        TimeGrain.THIRTY_MINUTES: "DATEADD(minute, DATEDIFF(minute, '2000-01-01', {col}) / 30 * 30, '2000-01-01')",  # noqa: E501
        TimeGrain.HOUR: "DATEADD(hour, DATEDIFF(hour, '2000-01-01', {col}), '2000-01-01')",  # noqa: E501
        TimeGrain.DAY: "DATEADD(day, DATEDIFF(day, '2000-01-01', {col}), '2000-01-01')",  # noqa: E501
        TimeGrain.WEEK: "DATEADD(week, DATEDIFF(week, '2000-01-01', {col}), '2000-01-01')",  # noqa: E501
        TimeGrain.MONTH: "DATEADD(month, DATEDIFF(month, '2000-01-01', {col}), '2000-01-01')",  # noqa: E501
        TimeGrain.QUARTER: "DATEADD(quarter, DATEDIFF(quarter, '2000-01-01', {col}), '2000-01-01')",  # noqa: E501
        TimeGrain.YEAR: "DATEADD(year, DATEDIFF(year, '2000-01-01', {col}), '2000-01-01')",  # noqa: E501
    }
