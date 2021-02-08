#region Imports

using System;
using System.Collections.Generic;
using System.Text;
using Statistics;
using Maths;

#endregion

namespace MonteCarlo {

    /** Method: 
    Haar Wavelet transform. Calculates the Haar step function and the Haar wavelet from two adjacent values.  
    For an array of values x0, x1, x2 ... xn, the calculation is for two adjacent points, x0 and x1:
    HaarStep = (x0 + x1)/2  (average) and HaarWave = (x0 - x1)/2  (average difference)
    This yields two vectors: HaarStep and HaarWave values.
    Result: the Haar value and a set of coefficients ordered by increasing frequency. */
    internal class Wavelets : SignalProc {

        #region Fields

        private double stepValue;
        private List<double[]> coeffs;
        private int addCount = 0;
        private StatFunctions stat;
        private List<double> noise;
        private double noiseMean;
        private double stationarity;
        private double stdRelError;
        private double trendMean;
        private double trendStdDev;
        private List<double> amplitudes;
        private List<double> frequencies;
        private double freqMean;
        private Dictionary<int, List<double>> freqDescomp;
        private Dictionary<int, List<double>> scaleDescomp;


        #endregion

        #region Constructor

        /** Method:  Constructor  */
        internal Wavelets() {
            this.coeffs = new List<double[]>();
            this.stat = new StatFunctions();
        }

        #endregion

        #region Properties

        /** Method:  Result Step Value  */
        internal double StepValue
        {
            get { return stepValue; }
        }

        /** Method:  Haar Coefficents  */
        internal List<double[]> Coeffs
        {
            get { return coeffs; }
        }

        /** Method:  Noise time series  */
        internal List<double> Noise
        {
            get { return noise; }
        }

        /** Method:  Mean of noise time series  */
        internal double NoiseMean
        {
            get { return noiseMean; }
        }

        /** Method:  Stationarity level  */
        internal double Stationarity
        {
            get { return stationarity; }
        }

        /** Method:  Std relative error  */
        internal double StdRelError
        {
            get { return stdRelError; }
        }

        /** Method:  Mean of trend time series  */
        internal double TrendMean
        {
            get { return trendMean; }
        }

        /** Method:  Standard deviation of trend time series   */
        internal double TrendStdDev
        {
            get { return trendStdDev; }
        }

        /** Method:  List of amplitudes for each period  */
        internal List<double> Amplitudes
        {
            get { return amplitudes; }
        }

        /** Method:  List of frequencies for each period  */
        internal List<double> Frequencies
        {
            get { return frequencies; }
        }

        /** Method:  Mean of frequencies  */
        internal double FreqMean
        {
            get { return freqMean; }
        }

        #endregion

        #region Internal Methods

        #region Calculate

        /** Method:  Direct Calculation of Haar Transform  */
        internal void CalcDirect()
        {

            if (trend == null || trend.Count == 0) { return; }

            this.coeffs.Clear();
            stepValue = haarCalc(trend.ToArray());
            coeffs.Reverse(); //from low to high frequency
        }

        /** Method:  Inverse Calculation of Haar Transform overwriting original data  */

        internal void CalcInverse()
        {
            if (data == null || data.Count == 0 || coeffs == null || coeffs.Count <= 0) { return; }

            trend[0] = stepValue;
            int exp2 = (int)Math.Log(trend.Count, 2);
            double[] spectrum;
            int wavLen, c;

            int s = 0;
            for (int e = exp2 - 1; e >= 0; e--)
            {
                wavLen = (int)Math.Pow(2, e);
                spectrum = coeffs[s];
                c = 0;
                while (wavLen * (2 * c + 1) < trend.Count)
                {
                    trend[wavLen * (2 * c + 1)] = trend[wavLen * (2 * c)] - spectrum[c];
                    trend[wavLen * (2 * c)] = trend[wavLen * (2 * c)] + spectrum[c];
                    c++;
                }
                s++;
            }
        }

        #endregion

        #region Measures

        /** Method:  Calculate statistics  */
        internal void CalcMeasures()
        {

            //noise
            noise = new List<double>();
            for (int i = 0; i < data.Count; i++)
            {
                noise.Add(data[i] - trend[i]);
            }

            //List<double> trend1 = new List<double>(trend);
            //trend = noise;
            //NoiseFilter(1);
            //List<double> trend2 = new List<double>(trend);
            //trend.Clear();
            //for(int i=0;i<trend1.Count;i++) {
            //    trend.Add(trend1[i] + trend2[i]);
            //}


            //noise mean
            noiseMean = stat.Mean(noise.ToArray());

            //stationarity
            Functions func = new Functions();
            stationarity = stat.AverageSlope(noise);

            //stdRelError
            double totNoise = 0;
            double totData = 0;
            for (int i = 0; i < data.Count; i++)
            {
                totNoise += Math.Abs(noise[i]);
                totData += data[i];
            }
            stdRelError = totNoise / totData;

            //mean and stdDev
            double[] trendArr = trend.ToArray();
            trendMean = stat.Mean(trendArr);
            trendStdDev = Math.Sqrt(stat.VarMuestral(trendArr));

            //frequencies
            frequencies = new List<double>();
            amplitudes = new List<double>();
            double freq = 1.0;
            double amp;
            for (int i = 0; i < trend.Count; i++)
            {
                if (i > 0 && trend[i] == trend[i - 1]) { freq++; }
                else { frequencies.Add(freq); freq = 1.0; }
            }
            frequencies.Add(freq);
            freqMean = stat.Mean(frequencies.ToArray());

            for (int i = 0; i < trend.Count; i++)
            {
                amp = CalcAmplitude(freqMean, trend[i]);
                amplitudes.Add(amp);
            }
        }

        private double CalcAmplitude(double x, double y)
        {
            return Math.Sqrt(x * x + y * y);
        }

        #endregion

        #region Debugging Methods

        /** Method:  Write the final Haar step value and the coefficients  */
        internal void WriteCoeffs()
        {
            if (coeffs == null || data.Count == 0) { System.Diagnostics.Debug.WriteLine(""); return; }

            System.Diagnostics.Debug.Write("[" + stepValue + "] : ");
            double[] a;
            for (int i = 0; i < coeffs.Count; i++)
            {
                System.Diagnostics.Debug.Write(" , ");
                a = coeffs[i];
                for (int j = 0; j < a.Length; j++)
                {
                    System.Diagnostics.Debug.Write(a[j]);
                    if (j < a.Length - 1) { System.Diagnostics.Debug.Write("  "); }
                }
            }
            System.Diagnostics.Debug.WriteLine("");
        }


        /** Method:  Write the data values used to generate the haar transform, and the coefficients in increasing frequency  */
        internal void WriteValues()
        {
            if (data == null || data.Count == 0) { System.Diagnostics.Debug.WriteLine(""); return; }
            for (int i = 0; i < data.Count; i++)
            {
                System.Diagnostics.Debug.Write(data[i]);
                if (i < data.Count - 1) { System.Diagnostics.Debug.Write("  "); }
            }
        }

        #endregion

        #endregion

        #region Private Methods

        #region Scale Descomposition

        /** Method:  Calculate scale descomposition (Haar algorithm)  */
        internal void CalcScaleDescomposition()
        {
            scaleDescomp = new Dictionary<int, List<double>>();
            PadLeft();
            CalcDirect();
            List<double> origTrend = new List<double>(trend);
            List<double[]> origCoeffs = Clone(coeffs);

            for (int i = 0; i < coeffs.Count; i++)
            {
                for (int j = 0; j < coeffs.Count; j++)
                {
                    if (j != i)
                    {
                        for (int k = 0; k < coeffs[j].Length; k++) { coeffs[j][k] = 0.0; }
                    }
                }
                CalcInverse();
                UnPadLeft();
                scaleDescomp.Add(i, trend);
                trend = new List<double>(origTrend);
                coeffs = Clone(origCoeffs);
            }
        }

        /** Method:  Obtain the scale descomposition of a particular spectrum  spec */
        internal List<double> GetScaleDescomposition(int spec)
        {
            if (scaleDescomp == null || !scaleDescomp.ContainsKey(spec)) { return new List<double>(); }
            return scaleDescomp[spec];
        }

        private List<double[]> Clone(List<double[]> orig)
        {
            List<double[]> clone = new List<double[]>();
            double[] arrayClone;
            foreach (double[] array in orig)
            {
                arrayClone = new double[array.Length];
                for (int i = 0; i < array.Length; i++) { arrayClone[i] = array[i]; }
                clone.Add(arrayClone);
            }
            return clone;
        }

        #endregion

        #region Freq Descomposition

        /** Method:  Calculate frequency descompostion  */
        internal void CalcFreqDescomposition()
        {
            freqDescomp = new Dictionary<int, List<double>>();
            PadLeft();
            CalcDirect();
            List<double> origTrend = new List<double>(trend);
            List<double[]> origCoeffs = Clone(coeffs);

            for (int i = 0; i < coeffs.Count; i++)
            {
                for (int j = 0; j < coeffs.Count; j++)
                {
                    if (j > i)
                    {
                        for (int k = 0; k < coeffs[j].Length; k++) { coeffs[j][k] = 0.0; }
                    }
                }
                CalcInverse();
                UnPadLeft();
                freqDescomp.Add(i, trend);
                trend = new List<double>(origTrend);
                coeffs = Clone(origCoeffs);
            }
        }

        /** Method:  Calculate frequency descomposition of a particular spectrum spec */
        internal List<double> GetFreqDescomposition(int spec)
        {
            if (freqDescomp == null || !freqDescomp.ContainsKey(spec)) { return new List<double>(); }
            return freqDescomp[spec];
        }

        /** Method:  Calculate defferential frequency descomposition of a particular spectrum spec  */
        internal List<double> GetFreqDiffDescomposition(int spec)
        {
            List<double> diff = new List<double>();
            if (spec == 0) { return GetFreqDescomposition(0); }
            if (freqDescomp == null || !freqDescomp.ContainsKey(spec)) { return diff; }
            List<double> freq = GetFreqDescomposition(spec);
            List<double> freqAnt = GetFreqDescomposition(spec - 1);
            for (int i = 0; i < freq.Count; i++) { diff.Add(freq[i] - freqAnt[i]); }
            return diff;
        }

        #endregion

        #region Noise Filtering

        /** Method:  Noise filter 
       n -  number of spectrums ignored 
       denoiseThreshold -  threshold for noise filtering 
       method -  type of noise filtering */
        internal void NoiseFilter(int n, double denoiseThreshold, DenoiseMethodType method)
        {
            PadLeft();
            CalcDirect();
            if (n > 0)
            {
                switch (method)
                {
                    case DenoiseMethodType.Hard: HardRemoveCoeffs(denoiseThreshold); break;
                    case DenoiseMethodType.Soft: SoftRemoveCoeffs(denoiseThreshold); break;
                    case DenoiseMethodType.NNGarrote: NNGarroteRemoveCoeffs(denoiseThreshold); break;
                    default:
                        throw new NotImplementedException();
                }
            }
            CalcInverse();
            UnPadLeft();
        }

        private void HardRemoveCoeffs(double denoiseThreshold)
        {
            foreach (double[] spec in coeffs)
            {
                for (int i = 0; i < spec.Length; i++)
                {
                    if (Math.Abs(spec[i]) < denoiseThreshold) { spec[i] = 0.0; }
                }
            }
        }

        private void SoftRemoveCoeffs(double denoiseThreshold)
        {
            double diff;
            foreach (double[] spec in coeffs)
            {
                for (int i = 0; i < spec.Length; i++)
                {
                    if (Math.Abs(spec[i]) < denoiseThreshold) { spec[i] = 0.0; }
                    else
                    {
                        diff = Math.Abs(spec[i]) - denoiseThreshold;
                        if (diff < 0) { diff = 0; }
                        if (spec[i] < 0) { spec[i] = -1.0 * diff; }
                        else { spec[i] = 1.0 * diff; }
                    }
                }
            }
        }

        private void NNGarroteRemoveCoeffs(double denoiseThreshold)
        {
            double diff;
            foreach (double[] spec in coeffs)
            {
                for (int i = 0; i < spec.Length; i++)
                {
                    if (Math.Abs(spec[i]) < denoiseThreshold) { spec[i] = 0.0; }
                    else
                    {
                        diff = 1.0 - denoiseThreshold / Math.Pow(spec[i], 2);
                        if (diff < 0) { diff = 0; }
                        spec[i] *= diff;
                    }
                }
            }
        }

        #endregion

        #region Pad Left

        private void PadLeft()
        {
            int count = trend.Count;
            int quadPow = 2;
            while (count > quadPow) { quadPow *= 2; }
            if (quadPow == count)
            {
                addCount = 0;
                return;
            }
            else
            {
                addCount = quadPow - count;
                double[] firstValues = new double[addCount];
                for (int i = 0; i < addCount; i++) { firstValues[i] = trend[i]; }
                double trimMean = stat.TrimMean(new List<double>(firstValues), 0.05, false);
                List<double> added = new List<double>();
                for (int i = 0; i < addCount; i++) { added.Add(trimMean); }
                added.AddRange(trend);
                trend = added;
            }
        }

        private void UnPadLeft()
        {
            for (int i = 0; i < addCount; i++) { trend.RemoveAt(0); }
        }

        /** Method:  Calculate the Haar transform. Result: an integer value and a list of coefficients from high to low frequencies. 
        values -  The number of elements in values must be a power of two */
        private double haarCalc(double[] values)
        {
            double retVal;
            double[] haarSteps = new double[values.Length / 2];
            double[] haarWaves = new double[values.Length / 2];

            for (int i = 0, j = 0; i < values.Length; i += 2, j++)
            {
                haarSteps[j] = (values[i] + values[i + 1]) / 2;
                haarWaves[j] = (values[i] - values[i + 1]) / 2;
            }
            coeffs.Add(haarWaves);

            if (haarSteps.Length == 1) { retVal = haarSteps[0]; }
            else { retVal = haarCalc(haarSteps); }
            return retVal;
        }

        #endregion

        #region Butterfly pattern

        //The inverse Haar function is calculated using a butterfly pattern to write into the data array.  An initial step writes the Haar value into data[0].  
        //In the case of the example below this would be data[0] = 5.0. Then a butterfly pattern is shown below.  Arrays indices start at 0, so in this example c[1,1] is the second element of the second coefficient vector.

        //wavelet:
        //{[5.0];
        //-3.0;
        //0.0, -1.0;
        //1.0, -2.0, 1.0, 0.0}

        //tmp = d[0];
        //d[0] = tmp + c[0, 0]
        //d[4] = tmp - c[0, 0]

        //tmp = d[0];
        //d[0] = tmp + c[1, 0]
        //d[2] = tmp - c[1, 0]
        //tmp = d[4];
        //d[4] = tmp + c[1, 1]
        //d[6] = tmp - c[1, 1]

        //tmp = d[0];
        //d[0] = tmp + c[2, 0]
        //d[1] = tmp - c[2, 0]
        //tmp = d[2];
        //d[2] = tmp + c[2, 1]
        //d[3] = tmp - c[2, 1]
        //tmp = d[4];
        //d[4] = tmp + c[2, 2]
        //d[5] = tmp - c[2, 2]
        //tmp = d[6];
        //d[6] = tmp + c[2, 3]
        //d[7] = tmp - c[2, 3]

        #endregion

        #endregion

        #region Enums

        /** Method:  Type of denoising method  */
        internal enum DenoiseMethodType
        {

            /** Method:  Hard denoise: Cuts off n spectrums  */
            Hard,

            /** Method:  Soft denoise: Cutts of values if less than threshold; etc  */
            Soft,

            /** Method:  NN Garrote: Mixed approach  */
            NNGarrote
        };

        #endregion


    }
}

