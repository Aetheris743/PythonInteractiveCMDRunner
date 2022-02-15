import subprocess
import threading
import queue

class script_interfate:
    def __init__(self, command="") -> None:
        self.proc = subprocess.Popen(command, 
            stdin=subprocess.PIPE, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            shell=True)
        self.q = queue.Queue()
        self.output_handle = threading.Thread(target=self.__scan_output, args=(self.proc.stdout, self.q))
        self.output_handle.daemon = True
        self.output_handle.start()

    def __scan_output(self, output, queue) -> None:
        for line in iter(output.readline, b''):
            queue.put(line)
        output.close()
    
    def write(self, command) -> None:
        self.proc.stdin.write((command +"\n").encode('utf-8'))
        self.proc.stdin.flush()

    def read(self) -> str:
        output = b"nothing found yet"
        try:
            output = self.q.get_nowait()
        except:
            pass
        return output.decode("utf-8")

    def close(self) -> None:
        self.proc.stderr.close()
        self.proc.stdin.close()
        self.proc.stdout.close()
        self.proc.terminate()

    def __get_queue_length(self) -> int:
        return self.q.qsize()

    def clear(self) -> None:
        with self.q.mutex:
            self.q.queue.clear()