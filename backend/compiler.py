import os
import subprocess
import io
import sys

def compile_c_to_binary(input_file, output_binary, target_arch):
    """
    Compiles a C file into a binary for the specified target architecture.
    """
    # Capture logs in a StringIO buffer
    log_buffer = io.StringIO()
    sys.stdout = log_buffer  # Redirect stdout to the buffer

    try:
        # Remove old binary if it exists
        if os.path.exists(output_binary):
            os.remove(output_binary)

        # Determine the compiler and flags based on the target architecture
        if target_arch == "aarch64":  # ARM64 (Apple Silicon or ARM 64-bit)
            compiler = "clang"
            flags = ["-target", "arm64-apple-macosx", "-o", output_binary, input_file]
        elif target_arch == "x86-64":  # x86-64 (Intel/AMD 64-bit)
            compiler = "clang"
            flags = ["-target", "x86_64-apple-macosx", "-o", output_binary, input_file]
        elif target_arch == "avr":  # AVR (Atmel microcontrollers)
            compiler = "avr-gcc"
            flags = [
                "-mmcu=atmega328p",  # Target microcontroller
                "-Os",              # Optimize for size
                "-o", output_binary,
                input_file
            ]
        else:
            raise ValueError(f"Unsupported architecture: {target_arch}")

        # Compile the C file
        compile_cmd = [compiler] + flags
        print(f"[INFO] Running: {' '.join(compile_cmd)}")
        subprocess.run(compile_cmd, check=True)
        print(f"[INFO] Binary generated: {output_binary}")

        # Generate HEX file for AVR
        if target_arch == "avr":
            hex_file = output_binary.replace(".elf", ".hex")
            subprocess.run(
                ["avr-objcopy", "-O", "ihex", "-R", ".eeprom", output_binary, hex_file],
                check=True
            )
            print(f"[INFO] HEX file generated: {hex_file}")
            output_file = hex_file
        else:
            output_file = output_binary

        # Get the logs from the buffer
        logs = log_buffer.getvalue()
        return output_file, logs

    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Compilation failed: {e}")
        logs = log_buffer.getvalue()
        raise RuntimeError(logs) from e
    except FileNotFoundError as e:
        print(f"[ERROR] Compiler not found: {e}")
        logs = log_buffer.getvalue()
        raise RuntimeError(logs) from e
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        logs = log_buffer.getvalue()
        raise RuntimeError(logs) from e
    finally:
        sys.stdout = sys.__stdout__  # Restore stdout
        log_buffer.close()