import subprocess

def _check_gpu_usage_nvidia_smi():
    try:
        # Run nvidia-smi to get GPU utilization
        result = subprocess.run([
            'nvidia-smi', 
            '--query-gpu=utilization.gpu,utilization.memory,encoder.stats.sessionCount,encoder.stats.averageFps',
            '--format=csv,noheader,nounits'
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            for i, line in enumerate(lines):
                parts = line.split(', ')
                if len(parts) >= 3:
                    encoder_sessions = parts[2] if parts[2] != '[Not Supported]' else '0'
                    if encoder_sessions != '0' and encoder_sessions != '[Not Supported]':
                        print(f" Active encoder sessions detected: {encoder_sessions}")
                        return True
        else:
            print(f" nvidia-smi failed: {result.stderr}")
            
    except subprocess.TimeoutExpired:
        print(" nvidia-smi timeout")
    except FileNotFoundError:
        print(" nvidia-smi not found in PATH")
    except Exception as e:
        print(f" nvidia-smi error: {e}")
    
    return False


def shadowplay_is_running() -> bool:
    """Returns True if shadowplay is already running, False if not."""
    results = {}
    
    results['nvidia_smi'] = _check_gpu_usage_nvidia_smi()
    
    for method, result in results.items():
        print(f"{method}: {result}")
    
    overall = any(results.values())
    
    return overall

if __name__ == "__main__":
    print(f"Shadowplay is running: {shadowplay_is_running()}")

