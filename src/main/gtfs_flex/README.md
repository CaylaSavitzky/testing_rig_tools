# gtfs_flex


the best entry point for this tool from the command line is probably process_flex_cli. 

a map produced by this tool can be overwhelmed by having too many stops, if that occurs just turn off the layers that those stops belongs to

the argument hideLegend or -h can be used to remove the legend when running the tool

sample:
--regular--
python3.11 process_flex_cli.py ~/Downloads/ ~/Downloads/output.html

--without legend--
python3.11 process_flex_cli.py  -hideLegend ~/Downloads/ ~/Downloads/output.html