# yabar-png-workspaces

This short program adds the functionality of pngs as workspaces to yabar.


To make it work properly, the images have to be in the right dimensions depending to the bar's dimensions.

You can assign keys to the workspaces in this program, but it will not bind these keys to the actual switching. This you have to manage on your own using xbindkeys or the window manager itself. It is just used to display the key next to the name of the workspace.

I do not ship any icons, you have to find icons on your own. You can find the icons I use on [Icons 8](https://www.icons8.com).

![screenshot](screenshot.png?raw=true "Screenshot")

### Yabar configuration

You have to add a block in yabar for each workspace (even if it is not displayed when inactive)

```

bar: {
	...
	block-list: ["ws1", "ws2"];
    
	ws1: {
		# where k # is the number the workspace this block is responsible for
		exec:"python /location/of/workspace.py -k 1";
		type: "persist";
		image: "/location/of/ws1_current.png";
		# you can also use image-shift/scale to center image, see yabar documentation
		background-color-argb:0x0;
		variable-size: true;
		pango-markup: true;
	}

	ws2: {
		# where k # is the number the workspace this block is responsible for
		exec:"python /location/of/workspace.py -k 2";
		type: "persist";
		image: "/location/of/ws2_current.png";
		# you can also use image-shift/scale to center image, see yabar documentation
		background-color-argb:0x0;
		variable-size: true;
		pango-markup: true;
	}
}

```
