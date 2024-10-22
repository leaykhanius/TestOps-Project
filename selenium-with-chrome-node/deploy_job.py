import os
import subprocess
import time
from kubernetes import client, config
from kubernetes.client.rest import ApiException

config.load_kube_config()

v1 = client.CoreV1Api()
apps_v1 = client.AppsV1Api()

def run_shell_command(command):
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        return output.decode("utf-8")
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e.output.decode('utf-8')}")
        return None

def apply_k8s_resource(resource_file):
    command = f"kubectl apply -f {resource_file}"
    result = run_shell_command(command)
    if result:
        print(f"Applied resource: {resource_file}")
    else:
        print(f"Failed to apply resource: {resource_file}")

def is_pod_ready(pod_name):
    try:
        pod_status = v1.read_namespaced_pod_status(pod_name, namespace="default")
        if pod_status.status.phase == "Running":
            return True
        else:
            return False
    except ApiException as e:
        print(f"Exception when reading pod status: {e}")
        return False

def deploy_resources(node_count):
    print("Deploying Test Case Controller Pod...")
    apply_k8s_resource("test-case-controller-deployment.yaml")
    print(f"Deploying {node_count} Chrome Node Pods...")
    command = f"kubectl scale deployment chrome-node --replicas={node_count}"
    run_shell_command(command)
    print("Deploying services...")
    apply_k8s_resource("chrome-node-service.yaml")
    apply_k8s_resource("test-case-controller-service.yaml")

def check_chrome_node_readiness(node_count):
    print(f"Checking if {node_count} Chrome Node Pods are ready...")
    for i in range(node_count):
        pod_name = f"chrome-node-{i}"
        retries = 0
        while not is_pod_ready(pod_name) and retries < 10:
            print(f"Waiting for {pod_name} to be ready...")
            time.sleep(5)
            retries += 1
        if retries == 10:
            print(f"{pod_name} is not ready after 10 retries. Exiting.")
            return False
    print(f"All {node_count} Chrome Node Pods are ready.")
    return True

def run_tests():
    print("Running test cases on Test Case Controller Pod...")
    result = run_shell_command("kubectl exec -it $(kubectl get pods -l app=test-case-controller -o jsonpath='{.items[0].metadata.name}') -- python3 run_tests.py")
    if result:
        print("Test execution completed successfully.")
    else:
        print("Test execution failed.")

def main():
    node_count = 3
    deploy_resources(node_count)
    if check_chrome_node_readiness(node_count):
        run_tests()
    else:
        print("Chrome Node Pods are not ready. Exiting.")

if __name__ == "__main__":
    main()

