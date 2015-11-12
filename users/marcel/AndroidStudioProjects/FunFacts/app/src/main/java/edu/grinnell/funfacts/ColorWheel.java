package edu.grinnell.funfacts;
import android.graphics.Color;

import java.util.Random;

/**
 * Created by Marcel on 11/5/2015.
 */
public class ColorWheel {
    // Member variables
    public String[] mColors = {
            "#39add1", // light blue
            "#3079ab", // dark blue
            "#c25975", // mauve
            "#e15258", // red
            "#f9845b", // orange
            "#838cc7", // lavender
            "#7d669e", // purple
            "#53bbb4", // aqua
            "#51b46d", // green
            "#e0ab18", // mustard
            "#637a91", // dark gray
            "#f092b0", // pink
            "#b7c0c7"  // light gray
    };

    private String mColor = "";

    // Return random color from mColors
    public int getColor(){

        Random randomGenerator = new Random();
        int number = randomGenerator.nextInt(mColors.length);
        mColor = mColors[number];
        return Color.parseColor(mColor);
    }
}

