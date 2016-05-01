% 1) choose a function: y = SOMEFUNC
% 
% 2) take n random x locations, calculate their corresponding y, store in 
%    y_act
% 
% 3) generate y_sim
% 
% 4) estimate with m-polynomial using [a_m, a_m-1 ... a0 ] = polyfit(x, y_sim, m),
%    t = 0:0.2:ceil(max(x)), y_fit = polyval(polyfit(x, y_sim, m), t)
close all
clear

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Generate k points for an actual function %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
n = 1000;
sigma = 1;

samples = [10 100 1000 10000];

colors = ['y' 'm' 'c' 'r' 'g' 'b'];

figure

for k = 1:length(samples)

    x = linspace(0.01, 0.99, samples(k))';
    %x = linspace(0, 10, samples(k))';

    % Choose a function ln(1/x) (log in matlab returns ln)
    % Choose because of taylor series -> higher polynomial should do better
    y_act = log(x.^-1);

    % OR
    % Choose a polynomial function
    % Choose to see whether there is a stagnation in performance for higher
    % order polynomials. Remember to change the linspace for x, and the limit
    % on the x-axis on the plot
    %y_act = 3 + 2*x + 0.4*x.^2 - x.^3;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Generate n datasets y_samp, sigma = 1 %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    y_samp = normrnd(repmat(y_act, 1, n), sigma);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Calculate variance etc, fit and plot with m-polynomial %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    A{1} = [ ones(samples(k), 1), x ];
    A{2} = [ ones(samples(k), 1), x, x.^2 ];
    A{3} = [ ones(samples(k), 1), x, x.^2 x.^3 ];
    A{4} = [ ones(samples(k), 1), x, x.^2 x.^3 x.^4 ];
    A{5} = [ ones(samples(k), 1), x, x.^2 x.^3 x.^4 x.^5 ];
    A{6} = [ ones(samples(k), 1), x, x.^2 x.^3 x.^4 x.^5 x.^6];
    
    subplot(2,2,k);
    xlim([0 1]);
    hold on;

    plot(x, y_act, 'k');
    for i = 1:length(A)
        
        % matlab returns a least squares solution here, since the matrix dimensions
        % will not match
        beta = A{i}\y_samp;
        y_hat = A{i} * beta;

        % bias and variance taken from page 50 of the book. Because we have
        % n datasets instead of one, I added an extra 'mean' around the 
        % definition: E_total = mean(E_T_i) forall i = 1:n
        bias_squared(i, k) = mean((y_act - mean(y_hat,2)).^2);
        variance(i, k) = mean(mean((y_hat - repmat(mean(y_hat, 2),1, n)).^2));
        
        % calculate the Mean Squared Error twice, once by adding bias and 
        % variance, and once by its definition, as a sanity check. Obviously,
        % the two should be equal
        mse(i, k) = bias_squared(i, k) + variance(i, k);
        mse2(i,k) = mean(mean((repmat(y_act, 1, n) - y_hat).^2));

        % plot one / the mean (comment out!) y_hat
        plot(x, y_hat(:,1), colors(i));
        %plot(x, mean(y_hat, 2), colors(i))
        title([num2str(samples(k)) ' samples']);
        xlabel('x');
        ylabel('y');
    end
end

bias_squared
variance
mse
mse2
