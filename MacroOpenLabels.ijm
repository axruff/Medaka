
dataset = "Medaka_1297_131-2";

//path = "201905_beamtime_medaka_stained";
path = "201912_beamtime_medaka";

setBatchMode("hide");

close("*");


run("TIFF Virtual Stack...", "open=/autofs/HD-LSDF/sd20d002/"+path+"/"+ dataset+"/brain_scaled_0.5_8bit_slices.tif");
rename("orig");

num_slices = nSlices;

start_slice = num_slices - round(num_slices * 0.35);
end_slice = num_slices - round(num_slices * 0.03);


run("Duplicate...", "duplicate range="+toString(start_slice)+"-"+toString(end_slice));
rename(dataset);

run("3-3-2 RGB");
//run("Brightness/Contrast...");
setMinAndMax(0, 12);
run("RGB Color");

selectWindow("orig");
close();




selectWindow(dataset);

run("Z Project...", "projection=[Standard Deviation]");
rename("proj");

selectWindow(dataset);
setSlice(round(nSlices / 2));

selectWindow("proj");

setBatchMode("exit and display");

//open("/autofs/HD-LSDF/sd20d002/201905_beamtime_medaka_stained/"+ dataset+"/brain_scaled_0.5_8bit_slices.tif");





//showMessage(slice);

//setSlice(slice);