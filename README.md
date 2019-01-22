# tk-katana
A Shotgun Engine for Katana

This engine provides Shotgun Toolkit integration for The Foundry's Katana.

It has been generously made public by Light Chaser Animation with help from The Foundry.

Thanks to Ying Jie Kong (Jerry) at Light Chaser and to Sam Saxon at the Foundry for their contributions.


## WWFX UK

Forked from [robblau's v0.1.0](https://github.com/robblau/tk-katana/tree/b9cca6e4009ff84870d6e691c2b25e818dc99d1a)
to hopefully make it production capable again for:

* Shotgun 8 and above
* Katana 3.0 
    * 3.1 uses PyQt5, yet to decide on how to go about it

### Patches by others

Some **initial** patches by other have been included early during this fork:

* Patches by RodeoFX up to [v0.1.1_rdo3](https://github.com/rodeofx/tk-katana/commit/0ddace4f285ff7f9642c165d3d225754584bbaf9)
* `AppCommand` changes by [Gael-Honorez-sb](https://github.com/Gael-Honorez-sb/tk-katana/commit/e06ab6b6b38960efbbdb18dc73b139aae278b040)

### Installation

**CURRENTLY INCOMPLETE**. Ideally, this would be as informative as the 
excellent [tk-natron](https://github.com/diegogarciahuerta/tk-natron) README

After [taking over the project configurations](https://support.shotgunsoftware.com/hc/en-us/articles/219039938-Pipeline-Tutorial#Taking%20Over%20the%20Project%20Config)

1. Locate where you installed the project configurations
1. Add this section to `config/env/includes/engine_locations.yml`
    ```yml
    # Katana
    engines.tk-katana.location:
    type: git
    path: https://github.com/wwfxuk/tk-katana.git
    branch: master
    ```
1. Then, create `config/env/includes/settings/tk-katana.yml`, placing this 
   inside:
    ```yml
    includes:
    # - ../app_locations.yml
    - ../engine_locations.yml
    # - ./tk-multi-loader2.yml
    # - ./tk-multi-publish2.yml
    # - ./tk-multi-screeningroom.yml
    # - ./tk-multi-shotgunpanel.yml
    # - ./tk-multi-snapshot.yml
    - ./tk-multi-workfiles2.yml    
    
    # shot_step
    settings.tk-katana.shot_step:
    apps:
        # tk-multi-about:
        #   location: "@apps.tk-multi-about.location"
        # tk-multi-breakdown:
        #   location: "@apps.tk-multi-breakdown.location"
        # tk-multi-setframerange:
        #   location: "@apps.tk-multi-setframerange.location"
        # tk-multi-loader2: "@settings.tk-multi-loader2.katana"
        # tk-multi-publish2: "@settings.tk-multi-publish2.katana.shot_step"
        # tk-multi-screeningroom: "@settings.tk-multi-screeningroom.rv"
        # tk-multi-shotgunpanel: "@settings.tk-multi-shotgunpanel.katana"
        # tk-multi-snapshot: "@settings.tk-multi-snapshot.katana.shot_step"
        tk-multi-workfiles2: "@settings.tk-multi-workfiles2.katana.shot_step"
    menu_favourites:
    # - {app_instance: tk-multi-workfiles2, name: File Open...}
    # - {app_instance: tk-multi-snapshot, name: Snapshot...}
    - {app_instance: tk-multi-workfiles2, name: File Save...}
    # - {app_instance: tk-multi-publish2, name: Publish...}
    location: '@engines.tk-katana.location'
    ```
1. Update the apps using the `tank` command in the project configurations 
   folder:
   ```sh
   ./tank cache_apps
   ```

