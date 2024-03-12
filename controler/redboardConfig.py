import RedBoard

r = RedBoard.RedBoard()


def loadConfig():
    defultConfig = "../config/redboard.yaml"


def generateConfig():
    print(r.config)
    # Write to file
    with open("../config/config.yaml", "w") as file:
        file.write(r.config)


if __name__ == "__main__":
    generateConfig()
