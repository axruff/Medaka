
//input_path = "Z:/tomo/ershov/medaka/KI_morph/"
//output_path = "Z:/tomo/ershov/medaka/KI_morph/";

//input_path = "/mnt/LSDF/tomo/ershov/medaka/KI_morph/";
//input_path = "/mnt/HD-LSDF/Medaka/201905_beamtime_medaka_stained/";
input_path = "/autofs/HD-LSDF/sd20d002/201905_beamtime_medaka_stained/";
output_path = "/mnt/LSDF/tomo/ershov/medaka/Classification/";


//datasets = newArray("803");

//datasets = newArray("509", "511", "513", "674", "672","673","803","1099", "1260", "1258");

//datasets = newArray("Medaka_802_4-2");

datasets = newArray(
"Medaka_800_4-1",
"Medaka_801_4-1",
"Medaka_802_4-2",
"Medaka_803_4-2",
"Medaka_804_4-2",
"Medaka_805_4-2",
"Medaka_806_7-2",
"Medaka_807_7-2",
"Medaka_808_7-2",
"Medaka_809_7-2",
"Medaka_810_7-2",
"Medaka_811_7-2",
"Medaka_812_7-2",
"Medaka_813_7-2",
"Medaka_814_8-2",
"Medaka_815_8-2",
"Medaka_816_8-2",
"Medaka_817_10-1",
"Medaka_818_10-1",
"Medaka_819_10-1",
"Medaka_820_10-1",
"Medaka_821_11-2",
"Medaka_822_11-2",
"Medaka_823_11-2",
"Medaka_824_11-2",
"Medaka_825_11-2",
"Medaka_826_11-2",
"Medaka_827_11-2",
"Medaka_828_11-2",
"Medaka_829_11-2",
"Medaka_830_13-2",
"Medaka_831_13-2",
"Medaka_832_13-2",
"Medaka_833_14-2",
"Medaka_834_14-2",
"Medaka_835_14-2",
"Medaka_836_15-1",
"Medaka_837_15-1",
"Medaka_838_15-1",
"Medaka_839_15-1",
"Medaka_840_15-1",
"Medaka_841_15-1",
"Medaka_842_17-1",
"Medaka_843_17-1",
"Medaka_844_17-1",
"Medaka_845_17-1",
"Medaka_846_17-1",
"Medaka_847_17-1",
"Medaka_848_17-1",
"Medaka_849_20-1",
"Medaka_850_22-1b",
"Medaka_851_22-1",
"Medaka_852_22-1",
"Medaka_853_22-1",
"Medaka_854_22-1",
"Medaka_855_22-1",
"Medaka_856_22-1",
"Medaka_857_23-2",
"Medaka_858_23-2",
"Medaka_859_23-2",
"Medaka_860_32-2",
"Medaka_861_32-2",
"Medaka_862_32-2",
"Medaka_863_32-2",
"Medaka_864_32-2",
"Medaka_865_32-2",
"Medaka_870_38-2",
"Medaka_871_38-2",
"Medaka_872_38-2",
"Medaka_873_38-2",
"Medaka_874_38-2",
"Medaka_875_38-2",
"Medaka_876_38-2",
"Medaka_877_38-2",
"Medaka_878_40-1",
"Medaka_879_40-1",
"Medaka_880_40-1",
"Medaka_881_40-1",
"Medaka_882_40-1",
"Medaka_883_40-1",
"Medaka_884_40-1",
"Medaka_885_40-1",
"Medaka_886_40-1",
"Medaka_887_40-2",
"Medaka_888_40-2",
"Medaka_889_40-2",
"Medaka_890_40-2",
"Medaka_891_40-2",
"Medaka_892_40-2",
"Medaka_893_40-2",
"Medaka_895_43-2",
"Medaka_897_43-2",
"Medaka_905_43-2",
"Medaka_906_43-2",
"Medaka_907_43-2",
"Medaka_908_43-2",
"Medaka_909_43-2",
"Medaka_910_43-2",
"Medaka_911_43-2",
"Medaka_912_43-2",
"Medaka_913_47-1",
"Medaka_914_47-1",
"Medaka_915_47-1",
"Medaka_916_47-1",
"Medaka_917_47-1",
"Medaka_918_47-1",
"Medaka_919_47-1",
"Medaka_920_47-1",
"Medaka_945_53-2",
"Medaka_946_53-2",
"Medaka_947_53-2",
"Medaka_948_53-2",
"Medaka_949_59-1",
"Medaka_950_59-1",
"Medaka_951_59-1",
"Medaka_952_60-1",
"Medaka_953_60-1",
"Medaka_954_60-1",
"Medaka_955_60-1",
"Medaka_956_60-1",
"Medaka_957_61-1",
"Medaka_958_61-1",
"Medaka_959_61-1",
"Medaka_960_62-2",
"Medaka_961_62-2",
"Medaka_962_62-2",
"Medaka_963_62-2",
"Medaka_964_62-2",
"Medaka_966_62-2",
"Medaka_967_68-1",
"Medaka_968_68-1",
"Medaka_969_68-1",
"Medaka_970_68-1",
"Medaka_971_69-2",
"Medaka_972_69-2",
"Medaka_974_69-2",
"Medaka_975_69-2",
"Medaka_976_70-2",
"Medaka_977_70-2",
"Medaka_978_70-2",
"Medaka_979_70-2");



angle = 30;

setBatchMode("hide");


for (d=0; d<datasets.length; d=d+1) {
	
	dataset = datasets[d];
	
	File.makeDirectory(output_path + "/" + dataset);
	

	//open(input_path + "volumes/" + dataset +".tif");
	//open(input_path + dataset +"/scaled_0.5_8bit_slices.tif");
	run("TIFF Virtual Stack...", "open=" + input_path + dataset+"/scaled_0.5_8bit_slices.tif");
	rename("orig_vol");
	
	num_slices = nSlices;
	start_slice = num_slices - round(num_slices * 0.35);
	end_slice = num_slices - round(num_slices * 0.03);
	
	run("Duplicate...", "duplicate range="+toString(start_slice)+"-"+toString(end_slice));
	rename("vol");
	
	//open(input_path + "brain/" + dataset +".tif");
	//open(input_path + dataset +"/brain_scaled_0.5_8bit_slices.tif");
	run("TIFF Virtual Stack...", "open=" + input_path + dataset+"/brain_scaled_0.5_8bit_slices.tif");
	rename("orig_label");
	run("Duplicate...", "duplicate range="+toString(start_slice)+"-"+toString(end_slice));
	run("3-3-2 RGB");
	setMinAndMax(0, 12);
	run("RGB Color");
	rename("label");
	
	r = 1;
	
	for (i=-3; i<=3; i=i+1) {
	//for (i=-1; i<=1; i=i+1) {
	
		rot = i*angle;
		
		
		//-------------------------------------------------
		// VOLUME
		//-------------------------------------------------
		
		selectWindow("vol");
		
		run("Duplicate...", "duplicate");
		//rename("dup");
		
		run("Rotate... ", "angle=" + toString(rot) + " grid=1 interpolation=Bilinear stack");
		rename("rot");
		
		run("Reslice [/]...", "output=1.000 start=Top avoid");
		rename("reslice");
		
		run("Z Project...", "projection=[Sum Slices]");
		
		//run("Brightness/Contrast...");
		//resetMinAndMax();
		//run("Enhance Contrast", "saturated=0.35");
		//setOption("ScaleConversions", true);
		run("8-bit");
		
		run("Flip Vertically");
		
		File.makeDirectory(output_path + "/" + dataset + "/" + "proj");
		saveAs("Tiff", output_path + "/" + dataset + "/" + "proj/" + dataset + "_proj" + "_rot" + IJ.pad(r, 3) + ".tif");
		rename("res");
		
		selectWindow("rot");
		close();
		
		selectWindow("reslice");
		close();
		
		selectWindow("res");
		close();
		
		
		//-------------------------------------------------
		// LABEL
		//-------------------------------------------------
		
		selectWindow("label");
		
		run("Duplicate...", "duplicate");
		//rename("dup");
		
		run("Rotate... ", "angle=" + toString(rot) + " grid=1 interpolation=Bilinear stack");
		rename("rot");
		
		run("Reslice [/]...", "output=1.000 start=Top avoid");
		rename("reslice");
		
		
		// Sum
		if (false) {
			selectWindow("reslice");
			run("Z Project...", "projection=[Sum Slices]");
			run("Flip Vertically");
			File.makeDirectory(output_path + "/" + dataset + "/" + "sum");
			saveAs("Tiff", output_path + "/" + dataset + "/" + "sum/" + dataset + "_sum" + "_rot" + IJ.pad(r, 3) + ".tif");
			close();
		}
		
		// Max
		selectWindow("reslice");
		run("Z Project...", "projection=[Max Intensity]");
		run("Flip Vertically");
		File.makeDirectory(output_path + "/" + dataset + "/" + "max");
		saveAs("Tiff", output_path + "/" + dataset + "/" + "max/" + dataset + "_max" + "_rot" + IJ.pad(r, 3) + ".tif");
		close();
		
		// Std
		selectWindow("reslice");
		run("Z Project...", "projection=[Standard Deviation]");
		run("Flip Vertically");
		File.makeDirectory(output_path + "/" + dataset + "/" + "std");
		saveAs("Tiff", output_path + "/" + dataset + "/" + "std/" + dataset + "_std" + "_rot" + IJ.pad(r, 3) + ".tif");
		close();
		
		
			
		selectWindow("rot");
		close();
		
		selectWindow("reslice");
		close();
		
		r = r+1;
		
		
	
	}
	
	selectWindow("vol");
	close();
	
	selectWindow("label");
	close();
	
	selectWindow("orig_vol");
	close();
	
	selectWindow("orig_label");
	close();
	

}

setBatchMode("exit and display");
showMessage("Finished!");


