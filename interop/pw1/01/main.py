import sys
import json
import re

def parse_payload(payload):
    # Remove any prefix and convert hex string to bytes if necessary
    if isinstance(payload, str):
        payload = payload.lower().replace("0x", "").replace(" ", "")
        # Convert from hex string to bytes
        try:
            if re.match(r"^[0-9a-f]+$", payload):
                payload = bytes.fromhex(payload)
            else:
                payload = payload.encode('latin1')
        except ValueError:
            sys.stderr.write("Error: Invalid payload format.\n")
            return None

    # Ensure payload length is exactly 8 bytes
    if len(payload) != 8:
        sys.stderr.write("Error: Payload length is not 8 bytes.\n")
        return None

    try:
        # Status
        status_byte = payload[0]
        status = status_byte & 0x01 # 1 byte => bit 1 => 0x00000001

        # Battery
        battery_byte = payload[1]
        nu = battery_byte & 0x0F # 1 byte => bits 3 to 0 => 0x00001111
        battery_voltage = (25 + nu) / 10.0

        # Temp
        temp_byte = payload[2]
        tau = temp_byte & 0x7F # 1 byte => bits 6 to 0 => 0x01111111
        temperature = tau - 32

        # Time
        time = int.from_bytes(payload[3:5], byteorder='little') # 2 bytes

        # Event count
        event_count = int.from_bytes(payload[5:8], byteorder='little') # 2 bytes

    except Exception as e:
        sys.stderr.write(f"Error while parsing payload: {e}\n")
        return None

    return {
        "Status": "occupied" if status else "unoccupied",
        "Battery": round(battery_voltage, 1),
        "Temperature": temperature,
        "Time": time,
        "Event Count": event_count
    }

def output_result(result, output_format):
    if output_format.lower() == "csv":
        print("Status,Battery,Temperature,Time Elapsed,Event Count")
        print(f"{result['Status']},{result['Battery']},{result['Temperature']},{result['Time']},{result['Event Count']}")
    elif output_format.lower() == "json":
        print(json.dumps(result, indent=4))
    else:
        sys.stderr.write("Error: Unsupported output format. Use 'csv' or 'json'.\n")

def main():
    inputs = [
        b"\x01\x09\x38\x0A\x00\x5A\x3D\x00",
        b"\x01\t8\n\x00Z=\x00",
        "0109380A005A3D00",
        "0x0109380A005A3D00",
    ]

    for payload in inputs:
        print(f"Processing payload: {payload}")
        
        output_format = sys.argv[1] if len(sys.argv) > 1 else "json"
        
        # Parse the payload
        result = parse_payload(payload)
        if result:
            output_result(result, output_format)
        else:
            sys.stderr.write("Failed to process payload.\n")

if __name__ == "__main__":
    main()
