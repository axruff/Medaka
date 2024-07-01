pathData = "/mnt/data/machine-learning/";
pathVolumes = pathData + "stained_xenopus/images/";
pathLabels = pathData + "stained_xenopus/masks/";

pathOutVolumes = pathData + "medaka_extended_train/images/";
pathOutLabels = pathData + "medaka_extended_train/masks/";

//dataset = "555";
//dataset_list = newArray("16");
//dataset_list = newArray("01","02","03","04","05","06","07","08","09","10","13","14","15","16","17","18","19","20","22","24");
dataset_list = newArray("01", "02");


zRot_list = newArray(25, 50, 75);
//yRot_list = newArray(25, 50, 75);
//xRot_list = newArray(25, 50, 75);

//zRot_list = newArray(-10, 10);
yRot_list = newArray(7, 15);
xRot_list = newArray(7, 15);

runLabels = true;
runVolumes = true;


setBatchMode("hide");

setBackgroundColor(0, 0, 0);

n_runs = zRot_list.length * yRot_list.length * xRot_list.length;
//showProgress(currentIndex, n_runs);

c = 0;

run("Close All");

for (d=0; d < dataset_list.length; d++)
{

	dataset = dataset_list[d];

	open(pathVolumes  + "st" + dataset +".tif");
	//run("Scale...", "x=0.5 y=0.5 z=0.5 interpolation=None average process create");
	rename("volume");

	open(pathLabels  + "st" + dataset +".tif");
	//run("Scale...", "x=0.5 y=0.5 z=0.5 interpolation=None average process create");
	rename("mask");

for (z=0; z < zRot_list.length-1; z++)
{
for (y=0; y < yRot_list.length-1; y++)
{
for (x=0; x < xRot_list.length-1; x++)
{

	showProgress(c, n_runs);

	// Process volumes

	if (runVolumes) 
	{
		selectWindow("volume");

		run("Duplicate...", "title=volume_temp duplicate");				
	
		run("Rotate... ", "angle="+toString(zRot_list[z])+" grid=1 interpolation=Bilinear fill stack");
		run("Reslice [/]...", "output=1.000 start=Top avoid");
		rename("rot_z");
			
		run("Rotate... ", "angle="+toString(yRot_list[y])+" grid=1 interpolation=Bilinear fill stack");
		run("Reslice [/]...", "output=1.000 start=Left avoid");
		rename("rot_y");
		
		run("Rotate... ", "angle="+toString(xRot_list[x])+" grid=1 interpolation=Bilinear fill stack");
		run("Reslice [/]...", "output=1.000 start=Left rotate avoid");
		rename("rot_x");

		selectWindow("rot_x");
		name = pathOutVolumes + "st" + dataset + "_rz" + toString(z+1) + "_ry" + toString(y+1) + "_rx" + toString(x+1) + ".tif";
		saveAs("Tiff", name);
		close();
	
		selectWindow("rot_z");
		close();

		selectWindow("rot_y");
		close();

		selectWindow("volume_temp");
		close();
	}
	
	// Process Labels
	if (runLabels) 
	{
		//open(pathLabels  + "st" + dataset +".tif");

		selectWindow("mask");

		run("Duplicate...", "title=mask_temp duplicate");
	
		run("Rotate... ", "angle="+toString(zRot_list[z])+" grid=1 interpolation=None fill stack");
		run("Reslice [/]...", "output=1.000 start=Top avoid");
		rename("rot_z");
		
		
		run("Rotate... ", "angle="+toString(yRot_list[y])+" grid=1 interpolation=None fill stack");
		run("Reslice [/]...", "output=1.000 start=Left avoid");
		rename("rot_y");
		
		run("Rotate... ", "angle="+toString(xRot_list[x])+" grid=1 interpolation=None fill stack");
		run("Reslice [/]...", "output=1.000 start=Left rotate avoid");
		rename("rot_x");

		
		selectWindow("rot_x");
		name = pathOutLabels + "st" + dataset + "_rz" + toString(z+1) + "_ry" + toString(y+1) + "_rx" + toString(x+1) + ".tif";
		saveAs("Tiff", name);
		close();
		
		
		selectWindow("rot_z");
		close();

		selectWindow("rot_y");
		close();

		selectWindow("mask_temp");
		close();
	}

	c = c+1;


	
	
}
}
}

selectWindow("volume");
close();

selectWindow("mask");
close();


}



//showMessage(pathData + pathVolumes + pathVolumes + dataset +".tiff");



showMessage("Finished!");



