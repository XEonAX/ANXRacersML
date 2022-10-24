import curses
import GymClient
from curseXcel import Table


def main(stdscr):
    client = GymClient.ANXRacersTelemetryClient()

    x = 0
    while x != "q":
        try:
            data = client.retrieve_data()
            table = Table(stdscr, 50, 2, 30, 60, 50, spacing=1, col_names=True)
            table.set_column_header("Info", 0)
            table.set_column_header("Value", 1)
            table.cols
            row = 0
            table.set_cell(0, 0, "LevelName")
            table.set_cell(0, 1, data[1].rstrip("\x00"))
            row = row + 1
            table.set_cell(row, 0, "Checkpoints")
            table.set_cell(row, 1, data[0][0])
            row = row + 1
            table.set_cell(row, 0, "Laps")
            table.set_cell(row, 1, data[0][1])
            row = row + 1
            table.set_cell(row, 0, "Difficulty")
            table.set_cell(row, 1, data[0][2])
            row = row + 1
            # table.refresh()

            # table = Table(stdscr, 11, 2,30, 120, 30, spacing=1, col_names=True)
            # table.set_column_header("ShipInfo",0)
            # table.set_column_header("Value",1)
            table.set_cell(row, 0, "ShipName")
            table.set_cell(row, 1, data[3].rstrip("\x00"))
            row = row + 1
            table.set_cell(row, 0, "Mass")
            table.set_cell(row, 1, "{:.5f}".format(data[2][0]))
            row = row + 1
            table.set_cell(row, 0, "LDrag")
            table.set_cell(row, 1, "{:.5f}".format(data[2][1]))
            row = row + 1
            table.set_cell(row, 0, "ADrag")
            table.set_cell(row, 1, "{:.5f}".format(data[2][2]))
            row = row + 1
            table.set_cell(row, 0, "SurgeForward")
            table.set_cell(row, 1, "{:.5f}".format(data[2][3]))
            row = row + 1
            table.set_cell(row, 0, "SurgeBackward")
            table.set_cell(row, 1, "{:.5f}".format(data[2][4]))
            row = row + 1
            table.set_cell(row, 0, "Strafe")
            table.set_cell(row, 1, "{:.5f}".format(data[2][5]))
            row = row + 1
            table.set_cell(row, 0, "Torque")
            table.set_cell(row, 1, "{:.5f}".format(data[2][6]))
            row = row + 1
            table.set_cell(row, 0, "Radius")
            table.set_cell(row, 1, "{:.5f}".format(data[2][7]))
            row = row + 1
            table.set_cell(row, 0, "Friction")
            table.set_cell(row, 1, "{:.5f}".format(data[2][8]))
            row = row + 1
            table.set_cell(row, 0, "Bounce")
            table.set_cell(row, 1, "{:.5f}".format(data[2][9]))

            row = row + 1
            table.set_cell(row, 0, "GameState")
            table.set_cell(row, 1, data[5])

            row = row + 1
            table.set_cell(row, 0, "Update No")
            table.set_cell(row, 1, data[6])


            
            row = row + 1
            table.set_cell(row, 0, "ShipState")
            table.set_cell(row, 1, "=========")
            row = row + 1
            table.set_cell(row, 0, "PosX")
            table.set_cell(row, 1, "{:.5f}".format(data[7][0]))
            row = row + 1
            table.set_cell(row, 0, "PosY")
            table.set_cell(row, 1, "{:.5f}".format(data[7][1]))
            row = row + 1
            table.set_cell(row, 0, "RotationZ")
            table.set_cell(row, 1, "{:.5f}".format(data[7][2]))
            row = row + 1
            table.set_cell(row, 0, "RotationW")
            table.set_cell(row, 1, "{:.5f}".format(data[7][3]))
            row = row + 1
            table.set_cell(row, 0, "VelocityX")
            table.set_cell(row, 1, "{:.5f}".format(data[7][4]))
            row = row + 1
            table.set_cell(row, 0, "VelocityY")
            table.set_cell(row, 1, "{:.5f}".format(data[7][5]))
            row = row + 1
            table.set_cell(row, 0, "AngularVelocity")
            table.set_cell(row, 1, "{:.5f}".format(data[7][6]))
            row = row + 1
            table.set_cell(row, 0, "InputY")
            table.set_cell(row, 1, "{:.5f}".format(data[7][7]))
            row = row + 1
            table.set_cell(row, 0, "InputZ")
            table.set_cell(row, 1, "{:.5f}".format(data[7][8]))
            
            row = row + 1
            table.set_cell(row, 0, "TrackState")
            table.set_cell(row, 1, "=========")
            row = row + 1
            table.set_cell(row, 0, "RelPosX")
            table.set_cell(row, 1, "{:.5f}".format(data[8][0]))
            row = row + 1
            table.set_cell(row, 0, "RelPosY")
            table.set_cell(row, 1, "{:.5f}".format(data[8][1]))
            row = row + 1
            table.set_cell(row, 0, "RotationZ")
            table.set_cell(row, 1, "{:.5f}".format(data[8][2]))
            row = row + 1
            table.set_cell(row, 0, "RotationW")
            table.set_cell(row, 1, "{:.5f}".format(data[8][3]))
            row = row + 1
            table.set_cell(row, 0, "Checkpoint")
            table.set_cell(row, 1, "{:.5f}".format(data[8][4]))

            table.refresh()
            match x:
                case "w":
                    client.set_inputs(1,0)
                case "a":
                    client.set_inputs(0,-1)
                case "s":
                    client.set_inputs(-1,0)
                case "d":
                    client.set_inputs(0,1)
                case _:
                    pass
        except AttributeError:
            print("Not Ready\r")
        stdscr.refresh()
        try:
            x = stdscr.getkey()
        except:
            a = 1


stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(True)
stdscr.nodelay(True)
curses.wrapper(main)

curses.nocbreak()
stdscr.keypad(False)
curses.echo()
curses.endwin()
