import yaml
import io
from os import path 


class rsConfig:

    # Config file location
    _rsConfigDefaultFile = "rsConfig.yml"


    # Define the default configuration structure.
    _default_config = {

        # Reddit Login credentials
        'credentials' : {
            'client_id' : '',
            'client_secret' : '',
            'user_agent' : '',

            # Username and password only needed if 'use_user_subs' equals true.
            'username' : '',
            'password' : ''
        },

        # Run time configs to adjust timing and filtering
        'run_time' : {   
                    
            'use_user_subs' : True, # Use logged-in user for sub list.
            'limit_sr' : 0,         # Limit number of subreddites to grab, 0 is unlimited.
            'default_entries' : 5,  # Default number of files to grab if not specified, per subreddit
            'max_attempts' : 50,    # Used to limit number of entries looked at. 
                                    # Usefull if sub only has .gif, and is unable to grab enough entries.  
            
            'time_between_runs': '12h', #Amount of time between 

            # Black and White List for allowed Subs
            'black_list_sub' : [],
            'white_list_sub' : [],
            # Additional Subreddits to grab from.
            'additional_sub' : [],
        },

        # Configs for where and how to store downloaded data.
        'output' : {
            'separate_by_sub': True,
            'output_folder' : 'Output/',
            'max_total_size': '1Gb',    # Limit total file download. Won't download more then this size, in total.
            'trim_files' : True,        # Trim files, by oldest, once max size reached.
        },

        # Configs to filter entries to download and sources.
        'filters' : {
            'allow_nsfw' : False,   # Is NFSW content allowed to be downloaded?
            'min_score' : 0,        # Minimum required reddit score. Posts below will be ignored.

            # Black and White List for allowed sources.
            'black_list_src' : [],
            'white_list_src' : [],

            # Black and White List for allowed file types. Don't add '.' to type.
            'black_list_file': [],
            'white_list_file': ['jpg', 'jpeg', 'png'],
        },   
    }


    def __init__(self):
       # Check if the config does not exist.
        if path.exists(self._rsConfigDefaultFile) != True:
            # Use the default config object to create the file.
            with io.open(self._rsConfigDefaultFile, 'w', encoding='utf8') as outfile:
                yaml.dump(self._default_config, outfile, default_flow_style=False, allow_unicode=True)
                self.currentConfig = None
        else:
            # File exists, so load it in.
            with io.open(self._rsConfigDefaultFile, 'r') as input:
                self.currentConfig = yaml.safe_load(input)

        # Create members for easy access to config
        if self.currentConfig != None:
            self.credentials = self.currentConfig['credentials']
            self.runtime = self.currentConfig['run_time']
            self.output = self.currentConfig['output']
            self.filters = self.currentConfig['filters']

