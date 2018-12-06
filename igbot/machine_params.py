machineSet = {
    "states" : [
        'user',
        'lobby',
        'instadp',
        'instadpinput',
        'printinstadp',
        'instadperror',
        'printdpserver',
        'igviewer',
        'iguploader',
        'viewig',
        'uploadprocess'
    ],
    "transitions" : [
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'lobby',
        },
        {
            'trigger': 'instadp_next',
            'source': 'instadp',
            'dest': 'instadpinput',
            'conditions': 'press_start'
        },
        {
            'trigger': 'instadp_next',
            'source': 'instadp',
            'dest': 'lobby',
            'conditions': 'press_return'
        },
        {
            'trigger': 'instadpinput_next',
            'source': 'instadpinput',
            'dest': 'printinstadp',
            'conditions': 'valid_id'
        },
        {
            'trigger': 'instadpinput_next',
            'source': 'instadpinput',
            'dest': 'instadperror',
            'conditions': 'invalid_id'
        },
        {
            'trigger': 'gobackinput',
            'source': 'instadperror',
            'dest': 'instadpinput',
        },
        {
            'trigger': 'instadpinput_next',
            'source': 'instadpinput',
            'dest': 'lobby',
            'conditions': 'press_return'
        },
        {
            'trigger': 'printdp_next',
            'source': 'printinstadp',
            'dest': 'instadpinput',
            'conditions': 'press_again'
        },
        {
            'trigger': 'printdp_next',
            'source': 'printinstadp',
            'dest': 'printdpserver',
            'conditions': 'press_upload'
        },
        {
            'trigger': 'gobackinput',
            'source': 'printdpserver',
            'dest': 'instadpinput',
        },
        {
            'trigger': 'lobby_next',
            'source': 'lobby',
            'dest': 'instadp',
            'conditions': 'is_instadp'
        },
        {
            'trigger': 'lobby_next',
            'source': 'lobby',
            'dest': 'iguploader',
            'conditions': 'is_contribute'
        },
        {
            'trigger': 'lobby_next',
            'source': 'lobby',
            'dest': 'igviewer',
            'conditions': 'is_view'
        },
        {
            'trigger': 'igviewer_next',
            'source': 'igviewer',
            'dest': 'lobby',
            'conditions': 'press_return'
        },
        {
            'trigger': 'iguploader_next',
            'source': 'iguploader',
            'dest': 'lobby',
            'conditions': 'press_return'
        },
        {
            'trigger': 'igviewer_next',
            'source': 'igviewer',
            'dest': 'viewig',
            'conditions': 'not_return'
        },
        {
            'trigger':'gobackupload',
            'source': 'uploadprocess',
            'dest': 'iguploader',
        },
        {
            'trigger': 'iguploader_next',
            'source': 'iguploader',
            'dest': 'uploadprocess',
        },
        {
            'trigger': 'view_next',
            'source': 'viewig',
            'dest': 'viewig',
            'conditions': 'not_return'
        },
        {
            'trigger': 'view_next',
            'source': 'viewig',
            'dest': 'lobby',
            'conditions': 'press_return'
        },
                {
            'trigger': 'printdp_next',
            'source': 'printinstadp',
            'dest': 'lobby',
            'conditions': 'press_return'
        },
    ],
    "initial" : 'user',
    "auto_transitions" : False,
}