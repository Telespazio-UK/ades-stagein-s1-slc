# stagein
Custom stagein to get S1 SLC files in the ADES for EOEPCA
https://github.com/EOEPCA/proc-ades

This will read stac catalog jsons created with https://github.com/SpaceApplications/stac-cat-utils and copy the files maintaining the folder structure. It doesn't create a catalog.json at the moment
Example to add into the ADES:
```
      stagein:
        cwl: |
          cwlVersion: v1.0
          doc: "Run Stars for staging input data"
          class: CommandLineTool
          hints:
            DockerRequirement:
              dockerPull: gr4n0t4/stagein:0.1.3
            "cwltool:Secrets":
              secrets:
              - ADES_STAGEIN_AWS_SERVICEURL
              - ADES_STAGEIN_AWS_ACCESS_KEY_ID
              - ADES_STAGEIN_AWS_SECRET_ACCESS_KEY
          id: stars
          inputs:
            ADES_STAGEIN_AWS_SERVICEURL:
              type: string?
            ADES_STAGEIN_AWS_ACCESS_KEY_ID:
              type: string?
            ADES_STAGEIN_AWS_SECRET_ACCESS_KEY:
              type: string?
          outputs: {}
          baseCommand: ['/bin/bash', 'stagein.sh']
          requirements:
            InitialWorkDirRequirement:
              listing:
              - entryname: stagein.sh
                entry: |-
                  #!/bin/bash
                  export AWS__ServiceURL=$(inputs.ADES_STAGEIN_AWS_SERVICEURL)
                  export AWS_ACCESS_KEY_ID=$(inputs.ADES_STAGEIN_AWS_ACCESS_KEY_ID)
                  export AWS_SECRET_ACCESS_KEY=$(inputs.ADES_STAGEIN_AWS_SECRET_ACCESS_KEY)
                  url=$1
                  if curl --output /dev/null --silent --head --fail "$url"; then
                    echo "URL: $url"
                  else
                    echo "URL does not exist: $url"
                    exit 1
                  fi
                  python /run.py $url
            EnvVarRequirement:
              envDef:
                PATH: /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
            ResourceRequirement: {}
```
Docker image available in https://hub.docker.com/repository/docker/gr4n0t4/stagein/general