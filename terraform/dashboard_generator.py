import sys
import os
import io
import json
import copy

BASE_TEMPLATE = {
    "annotations": {
        "list": [
            {
                "builtIn": 1,
                "datasource": "-- Grafana --",
                "enable": True,
                "hide": True,
                "iconColor": "rgba(0, 211, 255, 1)",
                "name": "Annotations & Alerts",
                "type": "dashboard"
            }
        ]
    },
    "editable": True,
    "gnetId": None,
    "graphTooltip": 0,
    "id": None,
    "links": [],
    "panels": [
    ],
    "schemaVersion": 16,
    "style": "dark",
    "tags": [],
    "templating": {
        "list": []
    },
    "time": {
        "from": "now-6h",
        "to": "now"
    },
    "timepicker": {
        "refresh_intervals": [
            "5s",
            "10s",
            "30s",
            "1m",
            "5m",
            "15m",
            "30m",
            "1h",
            "2h",
            "1d"
        ],
        "time_options": [
            "5m",
            "15m",
            "1h",
            "6h",
            "12h",
            "24h",
            "2d",
            "7d",
            "30d"
        ]
    },
    "timezone": "",
    "title": "FoundationDB Cluster",
    "uid": None,
    "version": 0
}

PANEL_LEGEND = {
    "avg": False,
    "current": False,
    "max": False,
    "min": False,
    "show": True,
    "total": False,
    "values": False,
}

CPU_USAGE_TEMPLATE = {
    "aliasColors": {},
    "bars": False,
    "dashLength": 10,
    "dashes": False,
    "datasource": None,
    "description": "CPU usage for individual process in this cluster",
    "fill": 1,
    "gridPos": {
        "h": 12,
        "w": 24,
        "x": 0,
        "y": 0
    },
    "id": 1,
    "lines": True,
    "linewidth": 1,
    "links": [],
    "nullPointMode": "null",
    "percentage": False,
    "pointradius": 5,
    "points": False,
    "renderer": "flot",
    "seriesOverrides": [],
    "spaceLength": 10,
    "stack": False,
    "steppedLine": False,
    "targets": [
    ],
    "thresholds": [],
    "timeFrom": None,
    "timeShift": None,
    "title": "Process CPU Usage(Percentage)",
    "tooltip": {
        "shared": True,
        "sort": 0,
        "value_type": "individual"
    },
    "type": "graph",
    "xaxis": {
        "buckets": None,
        "mode": "time",
        "name": None,
        "show": True,
        "values": []
    },
    "yaxes": [
        {
            "format": "percent",
            "label": None,
            "logBase": 1,
            "max": "100",
            "min": "0",
            "show": True
        },
        {
            "format": "short",
            "label": None,
            "logBase": 1,
            "max": None,
            "min": None,
            "show": None
        }
    ],
    "yaxis": {
        "align": False,
        "alignLevel": False
    }
}

CPU_USAGE_TARGET = {
    "alias": "$tag_address($tag_role_names)",
    "groupBy": [
        {
            "params": [
                "10s"
            ],
            "type": "time"
        },
        {
            "params": [
                "address"
            ],
            "type": "tag"
        },
        {
            "params": [
                "role_names"
            ],
            "type": "tag"
        },
        {
            "params": [
                "0"
            ],
            "type": "fill"
        }
    ],
    "measurement": "fdb_cluster_process",
    "orderByTime": "ASC",
    "policy": "default",
    "refId": "A",
    "resultFormat": "time_series",
    "select": [
        [
            {
                "params": [
                    "cpu_usage_cores"
                ],
                "type": "field"
            },
            {
                "params": [],
                "type": "mean"
            },
            {
                "params": [
                    " * 100"
                ],
                "type": "math"
            }
        ]
    ],
    "tags": [
        {
            "key": "address",
            "operator": "=",
            "value": None # This used to select wanted process via: '10.0.1.101:4501'
        }
    ]
}

MEMORY_USAGE_ABSOLUTE = {
    "aliasColors": {},
    "bars": False,
    "dashLength": 10,
    "dashes": False,
    "datasource": None,
    "description": "Memory usages (absolute) of individual process in this cluster",
    "fill": 1,
    "gridPos": {
        "h": 12,
        "w": 12,
        "x": 0,
        "y": 12
    },
    "id": 2,
    "lines": True,
    "linewidth": 1,
    "links": [],
    "nullPointMode": "null",
    "percentage": False,
    "pointradius": 5,
    "points": False,
    "renderer": "flot",
    "seriesOverrides": [],
    "spaceLength": 10,
    "stack": False,
    "steppedLine": False,
    "targets": [],
    "thresholds": [],
    "timeFrom": None,
    "timeShift": None,
    "title": "Memory Usages(Absolute)",
    "tooltip": {
        "shared": True,
        "sort": 0,
        "value_type": "individual"
    },
    "type": "graph",
    "xaxis": {
        "buckets": None,
        "mode": "time",
        "name": None,
        "show": True,
        "values": []
    },
    "yaxes": [
        {
            "format": "mbytes",
            "label": None,
            "logBase": 1,
            "max": None,
            "min": "0",
            "show": True
        },
        {
            "format": "short",
            "label": None,
            "logBase": 1,
            "max": None,
            "min": None,
            "show": None
        }
    ],
    "yaxis": {
        "align": False,
        "alignLevel": None
    }
}

MEMORY_USAGE_ABSOLUTE_TARGET = {
    "alias": "$tag_address($tag_role_names)",
    "groupBy": [
        {
            "params": [
                "10s"
            ],
            "type": "time"
        },
        {
            "params": [
                "address"
            ],
            "type": "tag"
        },
        {
            "params": [
                "role_names"
            ],
            "type": "tag"
        },
        {
            "params": [
                "0"
            ],
            "type": "fill"
        }
    ],
    "measurement": "fdb_cluster_process",
    "orderByTime": "ASC",
    "policy": "default",
    "refId": "A",
    "resultFormat": "time_series",
    "select": [
        [
            {
                "type": "field",
                "params": [
                    "memory_used_bytes"
                ]
            },
            {
                "type": "mean",
                "params": []
            },
            {
                "type": "math",
                "params": [
                    " / 1048576"
                ]
            }
        ]
    ],
    "tags": [
        {
            "key": "address",
            "operator": "=",
            "value": None
        }
    ]
}

MEMORY_USAGE_PERCENTAGE = {
    "type": "graph",
    "title": "Memory Usage(Percentage)",
    "gridPos": {
        "x": 12,
        "y": 12,
        "w": 12,
        "h": 12
    },
    "id": 3,
    "datasource": None,
    "targets": [
    ],
    "renderer": "flot",
    "yaxes": [
        {
            "label": None,
            "show": True,
            "logBase": 1,
            "min": "0",
            "max": "100",
            "format": "percent"
        },
        {
            "label": None,
            "show": True,
            "logBase": 1,
            "min": None,
            "max": None,
            "format": "short"
        }
    ],
    "xaxis": {
        "show": True,
        "mode": "time",
        "name": None,
        "values": [],
        "buckets": None
    },
    "yaxis": {
        "align": False,
        "alignLevel": None
    },
    "lines": True,
    "fill": 1,
    "linewidth": 1,
    "dashes": False,
    "dashLength": 10,
    "spaceLength": 10,
    "points": False,
    "pointradius": 5,
    "bars": False,
    "stack": False,
    "percentage": False,
    "nullPointMode": "null",
    "steppedLine": False,
    "tooltip": {
        "value_type": "individual",
        "shared": True,
        "sort": 0
    },
    "timeFrom": None,
    "timeShift": None,
    "aliasColors": {},
    "seriesOverrides": [],
    "thresholds": [],
    "links": [],
    "description": "Memory Usage (Percentage) for individual process in this cluster"
}

MEMORY_USAGE_PERCENTAGE_TARGET = {
    "alias": "$tag_address($tag_role_names)",
    "policy": "default",
    "resultFormat": "time_series",
    "orderByTime": "ASC",
    "tags": [
        {
            "key": "address",
            "operator": "=",
            "value": "10.0.1.101:4500"
        }
    ],
    "groupBy": [
        {
            "type": "time",
            "params": [
                "10s"
            ]
        },
        {
            "type": "tag",
            "params": [
                "address"
            ]
        },
        {
            "type": "tag",
            "params": [
                "role_names"
            ]
        },
        {
            "type": "fill",
            "params": [
                "0"
            ]
        }
    ],
    "select": [
        [
            {
                "type": "field",
                "params": [
                    "memory_percentage"
                ]
            },
            {
                "type": "mean",
                "params": []
            }
        ]
    ],
    "refId": "A",
    "measurement": "fdb_cluster_process"
}

DISK_READ_IOPS = {
    "aliasColors": {},
    "bars": False,
    "dashLength": 10,
    "dashes": False,
    "datasource": None,
    "description": "Disk Read IOPS for individual process in this cluster",
    "fill": 1,
    "gridPos": {
        "h": 12,
        "w": 12,
        "x": 0,
        "y": 24
    },
    "id": 4,
    "lines": True,
    "linewidth": 1,
    "links": [],
    "nullPointMode": "null",
    "percentage": False,
    "pointradius": 5,
    "points": False,
    "renderer": "flot",
    "seriesOverrides": [],
    "spaceLength": 10,
    "stack": False,
    "steppedLine": False,
    "targets": [],
    "thresholds": [],
    "timeFrom": None,
    "timeShift": None,
    "title": "Disk IOPS(Read)",
    "tooltip": {
        "shared": True,
        "sort": 0,
        "value_type": "individual"
    },
    "type": "graph",
    "xaxis": {
        "buckets": None,
        "mode": "time",
        "name": None,
        "show": True,
        "values": []
    },
    "yaxes": [
        {
            "format": "ops",
            "label": None,
            "logBase": 1,
            "max": None,
            "min": "0",
            "show": True
        },
        {
            "format": "short",
            "label": None,
            "logBase": 1,
            "max": None,
            "min": None,
            "show": True
        }
    ],
    "yaxis": {
        "align": False,
        "alignLevel": None
    }
}

DISK_READ_IOPS_TARGET = {
    "alias": "$tag_address($tag_role_names)",
    "groupBy": [
        {
            "params": [
                "10s"
            ],
            "type": "time"
        },
        {
            "params": [
                "address"
            ],
            "type": "tag"
        },
        {
            "params": [
                "role_names"
            ],
            "type": "tag"
        },
        {
            "params": [
                "0"
            ],
            "type": "fill"
        }
    ],
    "measurement": "fdb_cluster_process",
    "orderByTime": "ASC",
    "policy": "default",
    "refId": "A",
    "resultFormat": "time_series",
    "select": [
        [
            {
                "params": [
                    "disk_reads_hz"
                ],
                "type": "field"
            },
            {
                "params": [],
                "type": "mean"
            }
        ]
    ],
    "tags": [
        {
            "key": "address",
            "operator": "=",
            "value": None
        }
    ]
}

DISK_WRITE_IOPS = {
    "aliasColors": {},
    "bars": False,
    "dashLength": 10,
    "dashes": False,
    "datasource": None,
    "description": "Disk Write IOPS for individual process in this cluster",
    "fill": 1,
    "gridPos": {
        "h": 12,
        "w": 12,
        "x": 12,
        "y": 24
    },
    "id": 5,
    "lines": True,
    "linewidth": 1,
    "links": [],
    "nullPointMode": "null",
    "percentage": False,
    "pointradius": 5,
    "points": False,
    "renderer": "flot",
    "seriesOverrides": [],
    "spaceLength": 10,
    "stack": False,
    "steppedLine": False,
    "targets": [],
    "thresholds": [],
    "timeFrom": None,
    "timeShift": None,
    "title": "Disk IOPS(Write)",
    "tooltip": {
        "shared": True,
        "sort": 0,
        "value_type": "individual"
    },
    "type": "graph",
    "xaxis": {
        "buckets": None,
        "mode": "time",
        "name": None,
        "show": True,
        "values": []
    },
    "yaxes": [
        {
            "format": "ops",
            "label": None,
            "logBase": 1,
            "max": None,
            "min": "0",
            "show": True
        },
        {
            "format": "short",
            "label": None,
            "logBase": 1,
            "max": None,
            "min": None,
            "show": True
        }
    ],
    "yaxis": {
        "align": False,
        "alignLevel": None
    }
}

DISK_WRITE_IOPS_TARGET = {
    "alias": "$tag_address($tag_role_names)",
    "groupBy": [
        {
            "params": [
                "10s"
            ],
            "type": "time"
        },
        {
            "params": [
                "address"
            ],
            "type": "tag"
        },
        {
            "params": [
                "role_names"
            ],
            "type": "tag"
        },
        {
            "params": [
                "0"
            ],
            "type": "fill"
        }
    ],
    "measurement": "fdb_cluster_process",
    "orderByTime": "ASC",
    "policy": "default",
    "refId": "A",
    "resultFormat": "time_series",
    "select": [
        [
            {
                "params": [
                    "disk_writes_hz"
                ],
                "type": "field"
            },
            {
                "params": [],
                "type": "mean"
            }
        ]
    ],
    "tags": [
        {
            "key": "address",
            "operator": "=",
            "value": None
        }
    ]
}

NETWORK_SEND_MIB = {
    "aliasColors": {},
    "bars": False,
    "dashLength": 10,
    "dashes": False,
    "datasource": None,
    "description": "Network Send Mib for individual process in the cluster",
    "fill": 1,
    "gridPos": {
        "h": 12,
        "w": 12,
        "x": 0,
        "y": 36
    },
    "id": 6,
    "lines": True,
    "linewidth": 1,
    "links": [],
    "nullPointMode": "null",
    "percentage": False,
    "pointradius": 5,
    "points": False,
    "renderer": "flot",
    "seriesOverrides": [],
    "spaceLength": 10,
    "stack": False,
    "steppedLine": False,
    "targets": [],
    "thresholds": [],
    "timeFrom": None,
    "timeShift": None,
    "title": "Network IOPS(Send Mib)",
    "tooltip": {
        "shared": True,
        "sort": 0,
        "value_type": "individual"
    },
    "type": "graph",
    "xaxis": {
        "buckets": None,
        "mode": "time",
        "name": None,
        "show": True,
        "values": []
    },
    "yaxes": [
        {
            "format": "ops",
            "label": None,
            "logBase": 1,
            "max": None,
            "min": "0",
            "show": True
        },
        {
            "format": "short",
            "label": None,
            "logBase": 1,
            "max": None,
            "min": None,
            "show": True
        }
    ],
    "yaxis": {
        "align": False,
        "alignLevel": None
    }
}

NETWORK_SEND_MIB_TARGET = {
    "alias": "$tag_address($tag_role_names)",
    "groupBy": [
        {
            "params": [
                "10s"
            ],
            "type": "time"
        },
        {
            "params": [
                "address"
            ],
            "type": "tag"
        },
        {
            "params": [
                "role_names"
            ],
            "type": "tag"
        },
        {
            "params": [
                "0"
            ],
            "type": "fill"
        }
    ],
    "measurement": "fdb_cluster_process",
    "orderByTime": "ASC",
    "policy": "default",
    "refId": "A",
    "resultFormat": "time_series",
    "select": [
        [
            {
                "params": [
                    "network_megabits_sent_hz"
                ],
                "type": "field"
            },
            {
                "params": [],
                "type": "mean"
            }
        ]
    ],
    "tags": [
        {
            "key": "address",
            "operator": "=",
            "value": None
        }
    ]
}

NETWORK_RECEIVE_MIB = {
    "aliasColors": {},
    "bars": False,
    "dashLength": 10,
    "dashes": False,
    "datasource": None,
    "description": "Network Received Mib for individual process in the cluster",
    "fill": 1,
    "gridPos": {
        "h": 12,
        "w": 12,
        "x": 12,
        "y": 36
    },
    "id": 7,
    "lines": True,
    "linewidth": 1,
    "links": [],
    "nullPointMode": "null",
    "percentage": False,
    "pointradius": 5,
    "points": False,
    "renderer": "flot",
    "seriesOverrides": [],
    "spaceLength": 10,
    "stack": False,
    "steppedLine": False,
    "targets": [],
    "thresholds": [],
    "timeFrom": None,
    "timeShift": None,
    "title": "Network IOPS(Received Mib)",
    "tooltip": {
        "shared": True,
        "sort": 0,
        "value_type": "individual"
    },
    "type": "graph",
    "xaxis": {
        "buckets": None,
        "mode": "time",
        "name": None,
        "show": True,
        "values": []
    },
    "yaxes": [
        {
            "format": "ops",
            "label": None,
            "logBase": 1,
            "max": None,
            "min": "0",
            "show": True
        },
        {
            "format": "short",
            "label": None,
            "logBase": 1,
            "max": None,
            "min": None,
            "show": True
        }
    ],
    "yaxis": {
        "align": False,
        "alignLevel": None
    }
}

NETWORK_RECEIVE_MIB_TARGET = {
    "alias": "$tag_address($tag_role_names)",
    "groupBy": [
        {
            "params": [
                "10s"
            ],
            "type": "time"
        },
        {
            "params": [
                "address"
            ],
            "type": "tag"
        },
        {
            "params": [
                "role_names"
            ],
            "type": "tag"
        },
        {
            "params": [
                "0"
            ],
            "type": "fill"
        }
    ],
    "measurement": "fdb_cluster_process",
    "orderByTime": "ASC",
    "policy": "default",
    "refId": "A",
    "resultFormat": "time_series",
    "select": [
        [
            {
                "params": [
                    "network_megabits_received_hz"
                ],
                "type": "field"
            },
            {
                "params": [],
                "type": "mean"
            }
        ]
    ],
    "tags": [
        {
            "key": "address",
            "operator": "=",
            "value": None
        }
    ]
}
TEMPLATE_COLLECTIONS = [(CPU_USAGE_TEMPLATE,
                         CPU_USAGE_TARGET),
                        (MEMORY_USAGE_ABSOLUTE,
                         MEMORY_USAGE_ABSOLUTE_TARGET),
                        (MEMORY_USAGE_PERCENTAGE,
                         MEMORY_USAGE_PERCENTAGE_TARGET),
                        (DISK_READ_IOPS,
                         DISK_READ_IOPS_TARGET),
                        (DISK_WRITE_IOPS,
                         DISK_WRITE_IOPS_TARGET),
                        (NETWORK_SEND_MIB,
                         NETWORK_SEND_MIB_TARGET),
                        (NETWORK_RECEIVE_MIB,
                         NETWORK_RECEIVE_MIB_TARGET)
                        ]


def generate_graph(instance_number, core_number):

    for template, target in TEMPLATE_COLLECTIONS:
        for instance in range(instance_number):
            for core in range(core_number):
                tar = copy.deepcopy(target)
                tar['tags'][0]['value'] = "10.0.1.%d:%d" % (101+instance, 4500+core)
                template['targets'].append(tar)
                template['legend'] = PANEL_LEGEND
        BASE_TEMPLATE['panels'].append(template)
    return BASE_TEMPLATE


def generate_dashboard(instance_number, core_number):
    template_path = os.path.join(os.curdir, 'conf/provisioning/dashboard_template.json')
    with io.open(template_path, encoding="utf-8", mode="w") as f:
        result = generate_graph(int(instance_number), int(core_number))
        content = json.dumps(result)
        f.write(unicode(content))
        exit(0)


if __name__ == "__main__":
    generate_dashboard(sys.argv[1], sys.argv[2])
