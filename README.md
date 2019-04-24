# WPC
wpc stands for word pronunciation file collector. This module is for download mp3 files from Dictionary site given words.

![wpc_diagram](./wpc_diagram.png)

# Usage

1. Create `words.txt` file under the root directory. words should be seperated line by line.
2. Execute the command below under the root directory:

    ```shell
    $ python wpc.py
    ```
3. It will start to download mp3 files under the `downloaded` directory.
4. Check auto-created `no_link.txt` files that has words failed to download.

# Test
run command below:

```shell
$ pytest
```