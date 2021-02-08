#region Imports

using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Statistics;
using Maths;

#endregion

namespace Statistics  {

    internal class ZChartFcst : TsForecast  {

        #region Fields

        private List<double> acum;
        private List<double> rolling;
        private Polynom poly;
        private Splines splines;
        private int rollingPrd;

        #endregion

        #region Constructor

        public ZChartFcst(int rollingPrd)   {
            this.rollingPrd = rollingPrd;
            this.fcstMethod = FcstMethodType.ZChart;
            this.acum = new List<double>();
            this.rolling = new List<double>();
            this.poly = new Polynom();
            this.splines = new Splines();
        }

        #endregion

        #region TsForecast Implementation

        public override void Calculate()  {
            this.acum = new List<double>();
            acum.Add(hist[0]);
            rolling.Add(0);
            for (int t = 1; t < hist.Count; t++)  {
                acum.Add(acum[t-1] + hist[t]);
                if (t >= rollingPrd)  {
                    double roll = 0;
                    for (int i = t; i >= t - rollingPrd; i--) { roll += hist[i]; }
                    rolling.Add(roll);
                }
                else {
                    rolling.Add(0);
                }
            }
        }

        public override double[] GetFcst(int horizon) {
            List<double> acumFcst = GetAcumFcst(horizon);
            double x1 = rolling.Count - 1;
            double x2 = rolling.Count + horizon;
            double y1 = rolling[rolling.Count-1];
            double y2 = acumFcst[acumFcst.Count - 1];

            fcst = new double[horizon];
            for (int t = 0; t <fcst.Length; t++) {
                double x = x1 + t + 1;
                fcst[t] = splines.Interpolar(x, x1, x2, y1, y2) / rollingPrd;
            }
            return fcst;
        }

        public override void SetModel(object model)  {
            throw new NotImplementedException();
        }

        public override object GetModel()  {
            throw new NotImplementedException();
        }
        
        #endregion

        #region Private Methods

        private List<double> GetAcumFcst(int horizon) { 
            List<double> x = new List<double>();
            for(int i=0;i<acum.Count;i++) { x.Add(i); }
            List<double> coeffs = poly.Regression(x, acum, 1);            
            x.Clear();
            for(int i=0;i<horizon;i++) { x.Add(i); }
            List<double> acumFcst = poly.GetRegValues(x, coeffs);
            return acumFcst;
        }

        #endregion

        #region Enums

       
        #endregion

    }
}

