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
                if len(parts) >= 4:
                    gpu_util = int(parts[0]) if parts[0] != '[Not Supported]' else 0
                    mem_util = int(parts[1]) if parts[1] != '[Not Supported]' else 0
                    encoder_sessions = parts[2] if parts[2] != '[Not Supported]' else '0'
                    encoder_fps = parts[3] if parts[3] != '[Not Supported]' else '0'
                    
                    print(f" GPU {i} - Util: {gpu_util}%, Memory: {mem_util}%, Encoder Sessions: {encoder_sessions}, FPS: {encoder_fps}")
                    
                    # this led to false positives
                    #if gpu_util > 15:
                    #    print(f" High GPU utilization detected: {gpu_util}%")
                    #    return True
                        
                    # Active encoder sessions definitely indicate recording
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
    
    print("Method (nvidia-smi):")
    results['nvidia_smi'] = _check_gpu_usage_nvidia_smi()
    
    for method, result in results.items():
        print(f"{method}: {result}")
    
    overall = any(results.values())
    
    return overall
