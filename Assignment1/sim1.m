% 1) choose a function: y = SOMEFUNC
% 
% 2) take n random x locations, calculate their corresponding y, store in 
%    y_act
% 
% 3) generate y_sim
% 
% 4) estimate with m-polynomial using [a_m, a_m-1 ... a0 ] = polyfit(x, y_sim, m),
%    t = 0:0.2:ceil(max(x)), y_fit = polyval(polyfit(x, y_sim, m), t)

clear
clc

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Generate k points for an actual function %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
n = 1000;
sigma = 1;

datasets = [10 100 1000];

for k = 1:length(datasets)

    x = linspace(0, 10, datasets(k))';

    % Choose a function y = 2 + 0.5x %
    y_act = 2 + 0.5*x;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Generate n datasets y_samp, sigma = 1 %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    y_samp = normrnd(repmat(y_act, 1, n), sigma);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Calculate variance etc, fit and plot with m-polynomial %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    A{1} = [ ones(datasets(k), 1) x ];
    A{2} = [ ones(datasets(k), 1), x, x.^2 ];
    A{3} = [ ones(datasets(k), 1), x, x.^2 x.^3 ];
    A{4} = [ ones(datasets(k), 1), x, x.^2 x.^3 x.^4 ];
    A{5} = [ ones(datasets(k), 1), x, x.^2 x.^3 x.^4 x.^5 ];
    A{6} = [ ones(datasets(k), 1), x, x.^2 x.^3 x.^4 x.^5 x.^6];

    for i = 1:length(A)
        
        % matlab returns a least squares solution here, since the matrix dimensions
        % will not match
        beta = A{i}\y_samp;

        y_hat = A{i} * beta;

        bias_squared(i, k) = mean((y_act - mean(y_hat,2)).^2);
        
    end
end

bias_squared
