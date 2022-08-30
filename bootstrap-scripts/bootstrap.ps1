# If your execution policy is causing issues, pretty sure
# it's not as simple as running a script... you'd need to
# change the execution policy before the script runs. So,
# put this in the README?
#
# Might want to link:
#   https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.security/set-executionpolicy?view=powershell-7.2
Set-ExecutionPolicy Unrestricted -Scope Process
