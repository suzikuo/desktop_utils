if __name__ == "__main__":
    import multiprocessing

    from kernel.run import run

    multiprocessing.freeze_support()
    run()
