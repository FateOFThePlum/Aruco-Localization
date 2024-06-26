from networktables import NetworkTables
import time

# Start the NetworkTables server
NetworkTables.setServerTeam(2550)
NetworkTables.initialize()

# Get the default table
table = NetworkTables.getTable("datatable")

print(" ")
print(NetworkTables.getRemoteAddress())

# Function to update values in the table
def update_table():
    x = 0
    y = 0
    while True:
        table.putNumber("x", x)
        table.putNumber("y", y)
        x += 0.05
        y += 1.0
        time.sleep(1)

if __name__ == "__main__":
    update_table()
