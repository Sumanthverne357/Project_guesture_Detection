import sys
import asyncio

from bleak import BleakClient, BleakScanner

ADDRESS = "84:FC:E6:00:B7:66"
SERVICE_UUID = "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
CHARACTERISTIC_UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"

async def main():
    client = None  # Initialize the client variable outside the try block
    device = await BleakScanner.find_device_by_address(ADDRESS)
    if device is None:
        print("could not find device with address ", ADDRESS)
        return
    else:
        print("Device Foundwith address ",ADDRESS)
    try:
        client = BleakClient(ADDRESS)

        # paired = await client.pair()
        # print(f"Paired: {paired}")
        await client.connect()
        print(f"Connected: {client.is_connected}")
        while True:
            data_bytes = await client.read_gatt_char(CHARACTERISTIC_UUID)
            data = bytearray.decode(data_bytes)
            print(data)
            #Call Function here with data as argument
            # await asyncio.sleep(1)

    except Exception as e:
        print(f"Error: {e}")
        await client.disconnect()
        unpaired = await client.unpair()
        print(f"UnPaired: {unpaired}")
    finally:
        if client and client.is_connected:
            disconnect = await client.disconnect()
            print(f"disconnected: {disconnect}")
            unpaired = await client.unpair()
            print(f"UnPaired: {unpaired}")

if __name__ == "__main__":
    asyncio.run(main())