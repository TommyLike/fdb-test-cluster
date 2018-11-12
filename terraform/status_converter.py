import subprocess
import json


def get_process_role(roles):
    role_names = [r['role'] for r in roles]
    return ','.join(role_names)


def convert_json_status(content):
    process_metrices = []
    try:
        json_obj = json.loads(content)
        # Get all processes
        processes = json_obj['cluster']['processes']
        for key, value in processes.items():
            value['process_id'] = key
            value['role_names'] = get_process_role(value['roles'])
            value['memory_percentage'] = float(value['memory']['used_bytes']) / value['memory']['limit_bytes'] * 100
            process_metrices.append(value)
        return json.dumps(process_metrices)
    except Exception as e:
        return content


if __name__ == "__main__":
    content = subprocess.check_output(['fdbcli', '--exec', 'status json'])
    print(convert_json_status(content))
