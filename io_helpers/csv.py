

def append_results(test, config):
    if config.ftp:
        u_TLS_ISO = test.u_ISO_TLS
        match config.case:
            case 'a':
                tp = f'full (case A, u_ms = {config.u_ms})'
            case 'b':
                tp = f'full (case B, u_p = {config.u_p})'
            case 'c':
                tp = f'full (case C)'
    if config.stp:
        u_TLS_ISO = ''
        tp = 'simplified'

    with open(config.csv, 'a') as f:
        f.write(f"{config.metadata['device']},"
                f"{config.metadata['manufacturer']},"
                f"{config.metadata['serial_number']},"
                f"{config.metadata['FW_version']},"
                f"{config.metadata['operator']},"
                f"{config.metadata['datetime']},"
                f"{config.current_dt},"
                f"{config.metadata['temp']},"
                f"{config.metadata['humidity']},"
                f"{config.metadata['pressure']},"
                f"{u_TLS_ISO},"
                f"{test.passed},"
                f"{config.alpha},"
                f"{test.u_t},"
                f"{tp},"
                f"\"{config.metadata['comment']}\"\n")
