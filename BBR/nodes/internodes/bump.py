from BBR.nodes.internodes.internodes import Internode
import sys
import time

class Bump ( Internode ):
    """Class describing bump module

    Bump regions:
        FL   F   FR
         --------- 
        |         |
    FLM |    ^    | FRM
        |    |    |
    RLM |    |    | RRM
        |         |
         ---------
        RL   R   RR
    """

    def __init__(self, 
            afferents, 
            efferents,              # efferent 0 = left side, 1 = right side
            polling_delay = 0.01,   # time interval for polling afferents
            firing_delay = 0.01     # time interval between efferent writes
            ):
        if not len(efferents) == 2:
            print(efferents)
            raise ValueError("Two efferents must be provided (for left and right clusters).")
        Internode.__init__(self, afferents, efferents)
        self._pd = polling_delay
        self._fd = firing_delay
        
    def msg_to_cmds(self, msg):
        if msg == 'F':
            cmd = ['srrrrrsfs', 'srrrrrsfffffs']
        elif msg == 'FL':
            cmd = ['srrrrrsfs', 'srrrrrsfffffs']
        elif msg == 'FR':
            cmd = ['srrrrrsfffffs','srrrrrsfs']
        elif msg == 'FLM':
            cmd = ['','']
        elif msg == 'FRM':
            cmd = ['','']
        elif msg == 'RLM':
            cmd = ['','']
        elif msg == 'RRM':
            cmd = ['','']
        elif msg == 'RL':
            cmd = ['sfffffsfffffs', 'sfffffsfs']
        elif msg == 'RR':
            cmd = ['sfffffsfs', 'sfffffsfffffs']
        elif msg == 'R':
            cmd = ['sfffffsfffffs', 'sfffffsfs']
        else:
            raise ValueError('nonsense message received by bump node')
        return cmd
           


    def read(self):
        # read from afferents;
        # return a string indicating bump region from first non-empty afferent
        msg = None
        for aff in self._afferents:
            try:
                if not aff.empty():
                    msg = aff.get()
                    break
            except queue.Empty:
                print("Queue empty")
                continue
        return msg


    def fire(self, cmds):
        left_cmds = list(cmds[0])
        right_cmds = list(cmds[1])
        left_cmds.reverse()
        right_cmds.reverse()
        tmp = max(len(left_cmds), len(right_cmds))
        for ii in range(tmp):
            try:
                lc = left_cmds.pop()
            except IndexError:
                lc = None
            try:
                rc = right_cmds.pop()
            except IndexError:
                rc = None
            if not lc is None:
                self._efferents[0].put(lc)
            if not rc is None:
                self._efferents[1].put(rc)
            time.sleep(self._pd)

            
    def cleanup(self):
        pass

    
    def run(self):
        while True:
            try:
                msg = self.read()
                if msg is not None:
                    cmds = msg_to_cmds(msg)
                    self.fire(cmds)
                time.sleep(self._pd)

            except:
                self.cleanup()
                break

        sys.exit(0)

