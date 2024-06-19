if __name__ == "__main__":
    import multiprocessing

    from kernel.run import run
    from kernel.share_value import InitShareValue

    multiprocessing.freeze_support()
    InitShareValue()
    run()
