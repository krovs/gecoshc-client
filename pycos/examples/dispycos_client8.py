# Run 'dispycosnode.py' program to start processes to execute computations sent
# by this client, along with this program.

# This example uses status messages and message passing to run 'setup' task at
# remote process to prepare it for processing jobs.

# Unlike in earlier versions of pycos, computations can now take time - even if
# computations don't "yield" to scheduler, pycos can still send/receive
# messages, respond to timer events in scheduler etc. In this case, computation
# is simulated with 'time.sleep' which blocks user pycos thread, but another
# (reactive) asytask thread processes network traffic, run scheduler tasks.
def compute_task(task=None):
    import time

    reply_task = yield task.receive()  # first message is reply task (send_requests) at client

    result = 0
    while True:
        n = yield task.receive()
        if n is None:  # end of requests
            reply_task.send(result)
            break
        # long-running computation (without 'yield') is simulated with
        # 'time.sleep'; during this time client may send messages to this task
        # (which will be received and put in this task's message queue) or this
        # task can send messages to client
        time.sleep(n)
        result += n


# -- code below is executed locally --

# client (local) task runs computations
def client_proc(njobs, task=None):
    # schedule client with the scheduler; scheduler accepts one client
    # at a time, so if scheduler is shared, the client is queued until it
    # is done with already scheduled clients
    if (yield client.schedule()):
        raise Exception('Could not schedule client')

    # send 5 requests to remote process (compute_task)
    def send_requests(rtask, task=None):
        # first send this local task (to whom rtask sends result)
        rtask.send(task)
        for i in range(5):
            # even if recipient doesn't use "yield" (such as executing long-run
            # client, or thread-blocking function such as 'time.sleep' as
            # in this case), the message is accepted by another scheduler
            # (netpycos.Pycos) at the receiver and put in recipient's message
            # queue
            rtask.send(random.uniform(10, 20))
            # assume delay in input availability
            yield task.sleep(random.uniform(2, 5))
        # end of input is indicated with None
        rtask.send(None)
        result = yield task.receive()  # get result
        print('    %s computed result: %.4f' % (rtask.location, result))

    for i in range(njobs):
        rtask = yield client.rtask(compute_task)
        if isinstance(rtask, pycos.Task):
            print('  job %d processed by %s' % (i, rtask.location))
            pycos.Task(send_requests, rtask)
        else:
            print('  ** job %s failed: %s' % (i, rtask))

    yield client.close()


if __name__ == '__main__':
    import random, sys
    import pycos
    import pycos.netpycos
    from pycos.dispycos import *

    # package client components
    client = Client([compute_task])
    # run n jobs
    pycos.Task(client_proc, 10 if len(sys.argv) < 2 else int(sys.argv[1]))
