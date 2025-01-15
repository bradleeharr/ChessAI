import logging
import logging.config

# In order of increasing verbosity:
# CRITICAL -> ERROR -> WARNING -> INFO -> DEBUG -> NOTSET
logging.basicConfig(level=logging.WARNING)

logger = logging.getLogger()