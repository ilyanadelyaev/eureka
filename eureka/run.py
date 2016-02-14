import os

import configure

import eureka.application


config_file = os.environ['CONFIGFILE']


app = eureka.application.Application(
    configure.Configuration.from_file(
        config_file
    ).configure()
)


if __name__ == '__main__':
    app.run()
